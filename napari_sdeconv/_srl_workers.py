from qtpy.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit,
                            QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout,
                            QPushButton)
import napari
from ._splugin import SNapariWorker, SNapariWidget, SProgressObserver

from sdeconv.deconv import (RichardsonLucy, PSFGaussian)


# ---------------- SRichardsonLucy2D ----------------
class SRichardsonLucy2DWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        napari_viewer.events.layers_change.connect(self._on_layer_change)

        self._input_layer_box = QComboBox()
        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._sigma_value = QLineEdit('1.5')
        self._sigma_label = QLabel('PSF sigma')

        self._niter_value = QLineEdit('20')
        self._niter_label = QLabel('Number of iterations')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel('Image layer'), 0, 0)
        layout.addWidget(self._input_layer_box, 0, 1)
        layout.addWidget(self._advanced_check, 1, 0, 1, 2)

        layout.addWidget(self._sigma_label, 2, 0)
        layout.addWidget(self._sigma_value, 2, 1)
        layout.addWidget(self._niter_label, 3, 0)
        layout.addWidget(self._niter_value, 3, 1)
        self.setLayout(layout)
        self._init_layer_list()
        self.toggle_advanced(False)

    def _init_layer_list(self):
        for layer in self.viewer.layers:
            if isinstance(layer, napari.layers.image.image.Image):
                self._input_layer_box.addItem(layer.name)

    def _on_layer_change(self, e):
        current_text = self._input_layer_box.currentText()
        self._input_layer_box.clear()
        is_current_item_still_here = False
        for layer in self.viewer.layers:
            if isinstance(layer, napari.layers.image.image.Image):
                if layer.name == current_text:
                    is_current_item_still_here = True
                self._input_layer_box.addItem(layer.name)
        if is_current_item_still_here:
            self._input_layer_box.setCurrentText(current_text)

    def state(self) -> dict:
        return {'name': 'SRichardsonLucy2D',
                'inputs': {'image': self._input_layer_box.currentText()},
                'parameters': {'sigma': float(self._sigma_value.text()),
                               'niter': float(self._niter_value.text())
                               },
                'outputs': ['image', 'Richardson Lucy 2D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        self.advanced.emit(value)
        self.is_advanced = value


class SRichardsonLucy2DWorker(SNapariWorker):
    def __init__(self, napari_viewer, widget):
        super().__init__(napari_viewer, widget)

        self.observer = SProgressObserver()
        self.observer.progress_signal.connect(self.progress)
        self.observer.notify_signal.connect(self.log)

        self._out_data = None

    def run(self):
        """Execute the processing"""
        self.observer.progress(1)
        state = self.widget.state()
        input_image_layer = state['inputs']['image']
        state_params = state['parameters']

        niter = state_params['niter']
        sigma = state_params['sigma']

        image = self.viewer.layers[input_image_layer].data
        scale = self.viewer.layers[input_image_layer].scale

        psf_obj = PSFGaussian([sigma, sigma], image.shape)
        psf = psf_obj.run()

        obj_ = RichardsonLucy(niter=niter)
        deconv_image = obj_.run(image, psf)

        self._out_data = {'data': deconv_image, 'scale': scale,
                          'name': 'Richardson Lucy 2D'}
        self.observer.progress(100)
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])


# ---------------- SRichardsonLucy3D ----------------
class SRichardsonLucy3DWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        napari_viewer.events.layers_change.connect(self._on_layer_change)

        self._input_layer_box = QComboBox()
        self._psf_layer_box = QComboBox()
        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._niter_value = QLineEdit('20')
        self._niter_label = QLabel('Number of iterations')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel('Image layer'), 0, 0)
        layout.addWidget(self._input_layer_box, 0, 1)
        layout.addWidget(QLabel('PSF layer'), 1, 0)
        layout.addWidget(self._psf_layer_box, 1, 1)
        layout.addWidget(self._advanced_check, 2, 0, 1, 2)

        layout.addWidget(self._niter_label, 3, 0)
        layout.addWidget(self._niter_value, 3, 1)
        self.setLayout(layout)
        self._init_layer_list()
        self.toggle_advanced(False)

    def _init_layer_list(self):
        for layer in self.viewer.layers:
            if isinstance(layer, napari.layers.image.image.Image):
                self._input_layer_box.addItem(layer.name)
                self._psf_layer_box.addItem(layer.name)

    def _on_layer_change(self, e):
        current_text = self._input_layer_box.currentText()
        psf_current_text = self._psf_layer_box.currentText()
        self._input_layer_box.clear()
        self._psf_layer_box.clear()
        is_current_item_still_here = False
        is_psf_current_item_still_here = False
        for layer in self.viewer.layers:
            if isinstance(layer, napari.layers.image.image.Image):
                if layer.name == current_text:
                    is_current_item_still_here = True
                self._input_layer_box.addItem(layer.name)
                if layer.name == psf_current_text:
                    is_psf_current_item_still_here = True
                self._psf_layer_box.addItem(layer.name)
        if is_current_item_still_here:
            self._input_layer_box.setCurrentText(current_text)
        if is_psf_current_item_still_here:
            self._psf_layer_box.setCurrentText(psf_current_text)

    def state(self) -> dict:
        return {'name': 'SRichardsonLucy3D',
                'inputs': {'image': self._input_layer_box.currentText(),
                           'psf': self._psf_layer_box.currentText()
                           },
                'parameters': {'niter': float(self._niter_value.text())
                               },
                'outputs': ['image', 'Richardson Lucy 3D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        self.advanced.emit(value)
        self.is_advanced = value


class SRichardsonLucy3DWorker(SNapariWorker):
    def __init__(self, napari_viewer, widget):
        super().__init__(napari_viewer, widget)

        self.observer = SProgressObserver()
        self.observer.progress_signal.connect(self.progress)
        self.observer.notify_signal.connect(self.log)

        self._out_data = None

    def run(self):
        """Execute the processing"""
        self.observer.progress(1)
        state = self.widget.state()
        input_image_layer = state['inputs']['image']
        psf_image_layer = state['inputs']['psf']
        state_params = state['parameters']

        niter = state_params['niter']

        image = self.viewer.layers[input_image_layer].data
        scale = self.viewer.layers[psf_image_layer].scale

        psf = self.viewer.layers[psf_image_layer].data

        obj_ = RichardsonLucy(niter=niter)
        deconv_image = obj_.run(image, psf)

        self._out_data = {'data': deconv_image, 'scale': scale,
                          'name': 'Richardson Lucy 3D'}
        self.observer.progress(100)
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])