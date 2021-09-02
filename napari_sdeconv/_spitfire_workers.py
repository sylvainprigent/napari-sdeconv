from qtpy.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit,
                            QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout,
                            QPushButton)
import napari
from ._splugin import SNapariWorker, SNapariWidget, SProgressObserver

from sdeconv.deconv import (PSFGaussian, SpitfireDeconv)


# ---------------- SRichardsonLucy2D ----------------
class Spitfire2DWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        napari_viewer.events.layers_change.connect(self._on_layer_change)

        self._input_layer_box = QComboBox()
        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._sigma_value = QLineEdit('1.5')
        self._sigma_label = QLabel('PSF sigma')

        self._regularization_value = QLineEdit('12')
        self._regularization_label = QLabel('Regularization')

        self._weighting_value = QLineEdit('0.9')
        self._weighting_label = QLabel('Weighting')

        self._model_value = QComboBox()
        self._model_value.addItem('HV')
        self._model_value.addItem('SV')
        self._model_label = QLabel('Model')

        self._niter_value = QLineEdit('200')
        self._niter_label = QLabel('Number of iterations')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel('Image layer'), 0, 0)
        layout.addWidget(self._input_layer_box, 0, 1)
        layout.addWidget(self._advanced_check, 1, 0, 1, 2)

        layout.addWidget(self._sigma_label, 2, 0)
        layout.addWidget(self._sigma_value, 2, 1)

        layout.addWidget(self._regularization_label, 3, 0)
        layout.addWidget(self._regularization_value, 3, 1)

        layout.addWidget(self._weighting_label, 4, 0)
        layout.addWidget(self._weighting_value, 4, 1)

        layout.addWidget(self._model_label, 5, 0)
        layout.addWidget(self._model_value, 5, 1)

        layout.addWidget(self._niter_label, 6, 0)
        layout.addWidget(self._niter_value, 6, 1)

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
        return {'name': 'Spitfire2D',
                'inputs': {'image': self._input_layer_box.currentText()},
                'parameters': {'sigma': float(self._sigma_value.text()),
                               'regularization': float(
                                   self._regularization_value.text()),
                               'weighting': float(self._weighting_value.text()),
                               'model': self._model_value.currentText(),
                               'niter': int(self._niter_value.text())
                               },
                'outputs': ['image', 'Spitfire 2D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        if value:
            self._weighting_value.setVisible(True)
            self._weighting_label.setVisible(True)
            self._model_value.setVisible(True)
            self._model_label.setVisible(True)
            self._niter_value.setVisible(True)
            self._niter_label.setVisible(True)
        else:
            self._weighting_value.setVisible(False)
            self._weighting_label.setVisible(False)
            self._model_value.setVisible(False)
            self._model_label.setVisible(False)
            self._niter_value.setVisible(False)
            self._niter_label.setVisible(False)
        self.advanced.emit(value)
        self.is_advanced = value


class Spitfire2DWorker(SNapariWorker):
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
        regularization = pow(2, -state_params['regularization'])
        weighting = state_params['weighting']
        model = state_params['model']

        image = self.viewer.layers[input_image_layer].data
        scale = self.viewer.layers[input_image_layer].scale

        psf_obj = PSFGaussian([sigma, sigma], image.shape)
        psf = psf_obj.run()

        deconv = SpitfireDeconv(regularization, weighting, model, niter)
        deconv_image = deconv.run(image, psf)

        self._out_data = {'data': deconv_image, 'scale': scale,
                          'name': 'Spitfire 2D'}

        self.observer.progress(100)
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])


# ---------------- Spitfire3D ----------------
class Spitfire3DWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        napari_viewer.events.layers_change.connect(self._on_layer_change)

        self._input_layer_box = QComboBox()
        self._psf_layer_box = QComboBox()
        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._regularization_value = QLineEdit('12')
        self._regularization_label = QLabel('Regularization')

        self._weighting_value = QLineEdit('0.9')
        self._weighting_label = QLabel('Weighting')

        self._model_value = QComboBox()
        self._model_value.addItem('HV')
        self._model_value.addItem('SV')
        self._model_label = QLabel('Model')

        self._niter_value = QLineEdit('200')
        self._niter_label = QLabel('Number of iterations')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel('Image layer'), 0, 0)
        layout.addWidget(self._input_layer_box, 0, 1)
        layout.addWidget(QLabel('PSF layer'), 1, 0)
        layout.addWidget(self._psf_layer_box, 1, 1)
        layout.addWidget(self._advanced_check, 2, 0, 1, 2)

        layout.addWidget(self._regularization_label, 3, 0)
        layout.addWidget(self._regularization_value, 3, 1)

        layout.addWidget(self._weighting_label, 4, 0)
        layout.addWidget(self._weighting_value, 4, 1)

        layout.addWidget(self._model_label, 5, 0)
        layout.addWidget(self._model_value, 5, 1)

        layout.addWidget(self._niter_label, 6, 0)
        layout.addWidget(self._niter_value, 6, 1)
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
                'parameters': {'regularization': float(
                                   self._regularization_value.text()),
                               'weighting': float(self._weighting_value.text()),
                               'model': self._model_value.currentText(),
                               'niter': int(self._niter_value.text())
                               },
                'outputs': ['image', 'Spitfire 3D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        if value:
            self._weighting_value.setVisible(True)
            self._weighting_label.setVisible(True)
            self._model_value.setVisible(True)
            self._model_label.setVisible(True)
            self._niter_value.setVisible(True)
            self._niter_label.setVisible(True)
        else:
            self._weighting_value.setVisible(False)
            self._weighting_label.setVisible(False)
            self._model_value.setVisible(False)
            self._model_label.setVisible(False)
            self._niter_value.setVisible(False)
            self._niter_label.setVisible(False)
        self.advanced.emit(value)
        self.is_advanced = value


class Spitfire3DWorker(SNapariWorker):
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
        regularization = pow(2, -state_params['regularization'])
        weighting = state_params['weighting']
        model = state_params['model']

        image = self.viewer.layers[input_image_layer].data
        scale = self.viewer.layers[input_image_layer].scale

        psf = self.viewer.layers[psf_image_layer].data

        print('run SpitfireDeconv')
        deconv = SpitfireDeconv(regularization, weighting, model, niter)
        deconv_image = deconv.run(image, psf)

        self._out_data = {'data': deconv_image, 'scale': scale,
                          'name': 'Spitfire 3D'}

        self.observer.progress(100)
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])
