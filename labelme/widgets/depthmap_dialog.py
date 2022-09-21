import PIL.Image
import PIL.ImageEnhance
from qtpy.QtCore import Qt
from qtpy import QtGui
from qtpy import QtWidgets

from .. import utils


class DepthmapDialog(QtWidgets.QDialog):
    def __init__(self, img, callback, parent=None):
        super(DepthmapDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Depthmap Clipping")
        self.first = True
        self.depth = None

        self.slider_depth = self._create_slider()

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Depth"), self.slider_depth)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)

        print(img.get_format_mimetype())

        print(PIL.Image.Image.getextrema(img))

        channels = len(img.split())
        print(channels)
        if channels > 3:
            r, g, b, a = img.split()
            img = PIL.Image.merge('RGB', (r, g, b))
            self.depth = a
            min, max = self.depth.getextrema()
            print("Found min and max depth info:")
            print("Min: " + str(min))
            print("Max: " + str(max))
            self.img = img
            self.callback = callback
            self.slider_depth.setRange(min, max)

        self.img = img

        self.callback = callback

    def onNewValue(self, value):
        clip_at_depth = self.slider_depth.value()

        img = self.img.copy()
        if self.depth:
            width, height = self.depth.size
        else:
            return

        pxs_img = img.load()
        pxs_depth = self.depth.load()

        for x in range(width):
            for y in range(height):
                if pxs_depth[x, y] > clip_at_depth:
                    pxs_img[x, y] = (0, 0, 0)

        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_slider(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, 150)
        slider.setValue(50)
        slider.valueChanged.connect(self.onNewValue)
        return slider
