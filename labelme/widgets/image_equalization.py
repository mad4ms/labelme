import PIL.Image
import PIL.ImageEnhance
import PIL.ImageOps
from qtpy.QtCore import Qt
from qtpy import QtGui
from qtpy import QtWidgets

from .. import utils


class ImageEqualization(QtWidgets.QDialog):
    def __init__(self, img, callback, parent=None):
        super(ImageEqualization, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Image Equalization")

        self.btn_equal = self._create_button()

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Equalization"), self.btn_equal)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def onBtnPressed(self):
        img = self.img
        channels = len(img.split())
        print(channels)
        if channels > 3:
            r, g, b, a = img.split()
            img = PIL.Image.merge('RGB', (r, g, b))

        img = PIL.ImageOps.equalize(img, mask=None)
        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_button(self):
        btn = QtWidgets.QPushButton()
        btn.setText("Equalize image histogram")
        btn.clicked.connect(self.onBtnPressed)
        return btn
