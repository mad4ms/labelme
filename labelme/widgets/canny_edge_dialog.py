import PIL.Image
import PIL.ImageEnhance
import PIL.ImageOps
from scipy import ndimage
from skimage import filters, color
import numpy as np

from qtpy.QtCore import Qt
from qtpy import QtGui
from qtpy import QtWidgets

from matplotlib import pyplot as plt

from .. import utils


class CannyEdgeDialog(QtWidgets.QDialog):
    def __init__(self, img, callback, parent=None):
        super(CannyEdgeDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Canny Edge Detector")

        self.slider_blur = self._create_slider()
        self.slider_threshold = self._create_slider()

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Gaussian Blur"), self.slider_blur)
        formLayout.addRow(self.tr("Canny Threshold"), self.slider_threshold)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def onNewValue(self, value):
        blur = self.slider_blur.value()
        threshold = self.slider_threshold.value()

        img = self.img
        img = PIL.ImageOps.equalize(img, mask=None)
        img_data_np = np.array(img)
        img_data_np = color.rgb2gray(img_data_np)
        img_blur = filters.gaussian(img_data_np, blur, multichannel=True)
        img_edges = filters.prewitt(img_blur)

        # img = PIL.ImageEnhance.Brightness(img).enhance(blur)
        # img = PIL.ImageEnhance.Contrast(img).enhance(threshold)
        print(img_edges.shape)
        # h, w, c = img_edges.shape
        # img_data = img_edges.tobytes()
        # img_data_np = np.array(img)

        # convert values to 0 - 255 int8 format
        formatted = (img_edges * 255 / np.max(img_edges)).astype('uint8')
        img = PIL.Image.fromarray(formatted)

        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)

        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_slider(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, 20)
        slider.setValue(1)
        slider.valueChanged.connect(self.onNewValue)
        return slider
