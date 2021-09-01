from qtpy.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit,
                            QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout,
                            QPushButton)
import napari
from ._splugin import SNapariWorker, SNapariWidget, SProgressObserver

from sdeconv.deconv import (PSFGaussian, PSFGibsonLanni)


# ---------------- SPSFGaussian2D ----------------
class SPSFGaussian2DWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._sigma_x_value = QLineEdit('1.5')
        self._sigma_x_label = QLabel('PSF sigma x')

        self._sigma_y_value = QLineEdit('1.5')
        self._sigma_y_label = QLabel('PSF sigma y')

        self._size_x_value = QLineEdit('128')
        self._size_x_label = QLabel('Image length')

        self._size_y_value = QLineEdit('128')
        self._size_y_label = QLabel('Image width')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._advanced_check, 0, 0, 1, 2)

        layout.addWidget(self._sigma_x_label, 1, 0)
        layout.addWidget(self._sigma_x_value, 1, 1)
        layout.addWidget(self._sigma_y_label, 2, 0)
        layout.addWidget(self._sigma_y_value, 2, 1)
        layout.addWidget(self._size_x_label, 3, 0)
        layout.addWidget(self._size_x_value, 3, 1)
        layout.addWidget(self._size_y_label, 4, 0)
        layout.addWidget(self._size_y_value, 4, 1)

        self.setLayout(layout)
        self.toggle_advanced(False)

    def state(self) -> dict:
        return {'name': 'SPSFGaussian2D',
                'inputs': {},
                'parameters': {'sigma_x': float(self._sigma_x_value.text()),
                               'sigma_y': float(self._sigma_y_value.text()),
                               'size_x': int(self._size_x_value.text()),
                               'size_y': int(self._size_y_value.text())
                               },
                'outputs': ['image', 'PSF Gaussian 2D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        self.advanced.emit(value)
        self.is_advanced = value


class SPSFGaussian2DWorker(SNapariWorker):
    def __init__(self, napari_viewer, widget):
        super().__init__(napari_viewer, widget)

        self.observer = SProgressObserver()
        self.observer.progress_signal.connect(self.progress)
        self.observer.notify_signal.connect(self.log)

        self._out_data = None

    def run(self):
        """Execute the processing"""
        state = self.widget.state()
        state_params = state['parameters']

        sigma_x = state_params['sigma_x']
        sigma_y = state_params['sigma_y']
        sx = state_params['size_x']
        sy = state_params['size_y']

        psf_obj = PSFGaussian([sigma_x, sigma_y], (sx, sy))
        psf = psf_obj.run()

        self._out_data = {'data': psf, 'scale': (1, 1),
                          'name': 'PSF Gaussian 2D'}

        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])


# ---------------- SPSFGaussian3D ----------------
class SPSFGaussian3DWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._sigma_x_value = QLineEdit('1.5')
        self._sigma_x_label = QLabel('PSF sigma x')

        self._sigma_y_value = QLineEdit('1.5')
        self._sigma_y_label = QLabel('PSF sigma y')

        self._sigma_z_value = QLineEdit('1.5')
        self._sigma_z_label = QLabel('PSF sigma z')

        self._size_x_value = QLineEdit('128')
        self._size_x_label = QLabel('Image length')

        self._size_y_value = QLineEdit('128')
        self._size_y_label = QLabel('Image width')

        self._size_z_value = QLineEdit('16')
        self._size_z_label = QLabel('Image depth')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._advanced_check, 0, 0, 1, 2)

        layout.addWidget(self._sigma_x_label, 1, 0)
        layout.addWidget(self._sigma_x_value, 1, 1)
        layout.addWidget(self._sigma_y_label, 2, 0)
        layout.addWidget(self._sigma_y_value, 2, 1)
        layout.addWidget(self._sigma_z_label, 3, 0)
        layout.addWidget(self._sigma_z_value, 3, 1)
        layout.addWidget(self._size_x_label, 4, 0)
        layout.addWidget(self._size_x_value, 4, 1)
        layout.addWidget(self._size_y_label, 5, 0)
        layout.addWidget(self._size_y_value, 5, 1)
        layout.addWidget(self._size_z_label, 6, 0)
        layout.addWidget(self._size_z_value, 6, 1)

        self.setLayout(layout)
        self.toggle_advanced(False)

    def state(self) -> dict:
        return {'name': 'SPSFGaussian3D',
                'inputs': {},
                'parameters': {'sigma_x': float(self._sigma_x_value.text()),
                               'sigma_y': float(self._sigma_y_value.text()),
                               'sigma_z': float(self._sigma_z_value.text()),
                               'size_x': int(self._size_x_value.text()),
                               'size_y': int(self._size_y_value.text()),
                               'size_z': int(self._size_z_value.text())
                               },
                'outputs': ['image', 'PSF Gaussian 3D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        self.advanced.emit(value)
        self.is_advanced = value


class SPSFGaussian3DWorker(SNapariWorker):
    def __init__(self, napari_viewer, widget):
        super().__init__(napari_viewer, widget)

        self.observer = SProgressObserver()
        self.observer.progress_signal.connect(self.progress)
        self.observer.notify_signal.connect(self.log)

        self._out_data = None

    def run(self):
        """Execute the processing"""
        state = self.widget.state()
        state_params = state['parameters']

        sigma_x = state_params['sigma_x']
        sigma_y = state_params['sigma_y']
        sigma_z = state_params['sigma_z']
        sx = state_params['size_x']
        sy = state_params['size_y']
        sz = state_params['size_z']

        psf_obj = PSFGaussian([sigma_x, sigma_y, sigma_z], (sx, sy, sz))
        psf = psf_obj.run()

        self._out_data = {'data': psf, 'scale': (1, 1, 1),
                          'name': 'PSF Gaussian 3D'}

        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])


# ---------------- SPSFGibsonLanni3D ----------------
class SPSFGibsonLanniWidget(SNapariWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self._advanced_check = QCheckBox('advanced')
        self._advanced_check.stateChanged.connect(self.toggle_advanced)

        self._size_x_value = QLineEdit('128')
        self._size_x_label = QLabel('Image length')
        self._size_y_value = QLineEdit('128')
        self._size_y_label = QLabel('Image width')
        self._size_z_value = QLineEdit('18')
        self._size_z_label = QLabel('Image depth')

        self._res_lateral_value = QLineEdit('100')
        self._res_lateral_label = QLabel('Lateral resolution')
        self._res_axial_value = QLineEdit('250')
        self._res_axial_label = QLabel('Axial resolution')
        self._numerical_aperture_value = QLineEdit('1.4')
        self._numerical_aperture_label = QLabel('Numerical aperture')
        self._lambda_value = QLineEdit('610')
        self._lambda_label = QLabel('Illumination wavelength')
        self._ti0_value = QLineEdit('150')
        self._ti0_label = QLabel('Working distance')
        self._ni_value = QLineEdit('1.5')
        self._ni_label = QLabel('Refractive index immersion')
        self._ns_value = QLineEdit('1.33')
        self._ns_label = QLabel('Refractive index sample')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._advanced_check, 0, 0, 1, 2)

        layout.addWidget(self._size_x_label, 1, 0)
        layout.addWidget(self._size_x_value, 1, 1)
        layout.addWidget(self._size_y_label, 2, 0)
        layout.addWidget(self._size_y_value, 2, 1)
        layout.addWidget(self._size_z_label, 3, 0)
        layout.addWidget(self._size_z_value, 3, 1)

        layout.addWidget(self._res_lateral_label, 4, 0)
        layout.addWidget(self._res_lateral_value, 4, 1)
        layout.addWidget(self._res_axial_label, 5, 0)
        layout.addWidget(self._res_axial_value, 5, 1)
        layout.addWidget(self._numerical_aperture_label, 6, 0)
        layout.addWidget(self._numerical_aperture_value, 6, 1)
        layout.addWidget(self._lambda_label, 7, 0)
        layout.addWidget(self._lambda_value, 7, 1)
        layout.addWidget(self._ti0_label, 8, 0)
        layout.addWidget(self._ti0_value, 8, 1)
        layout.addWidget(self._ni_label, 9, 0)
        layout.addWidget(self._ni_value, 9, 1)
        layout.addWidget(self._ns_label, 10, 0)
        layout.addWidget(self._ns_value, 10, 1)

        self.setLayout(layout)
        self.toggle_advanced(False)

    def state(self) -> dict:
        return {'name': 'SPSFGibsonLanni3D',
                'inputs': {},
                'parameters': {'sx': float(self._size_x_value.text()),
                               'sy': float(self._size_y_value.text()),
                               'sz': float(self._size_z_value.text()),
                               'res_lateral': float(self._res_lateral_value.text()),
                               'res_axial': float(self._res_axial_value.text()),
                               'numerical_aperture': float(self._numerical_aperture_value.text()),
                               'lambda': float(self._lambda_value.text()),
                               'ti0': float(self._ti0_value.text()),
                               'ni': float(self._ni_value.text()),
                               'ns': float(self._ns_value.text())
                               },
                'outputs': ['image', 'PSF Gibson-Lanni 3D']
                }

    def toggle_advanced(self, value):
        """Change the parameters widget to advanced mode"""
        self.advanced.emit(value)
        self.is_advanced = value


class SPSFGibsonLanniWorker(SNapariWorker):
    def __init__(self, napari_viewer, widget):
        super().__init__(napari_viewer, widget)

        self.observer = SProgressObserver()
        self.observer.progress_signal.connect(self.progress)
        self.observer.notify_signal.connect(self.log)

        self._out_data = None

    def run(self):
        """Execute the processing"""

        print('run ...')
        state = self.widget.state()
        state_params = state['parameters']

        print('get the parameters')

        sx = state_params['sx']
        sy = state_params['sy']
        sz = state_params['sz']
        res_lateral = state_params['res_lateral']
        res_axial = state_params['res_axial']
        numerical_aperture = state_params['numerical_aperture']
        lambda_ = state_params['lambda']
        ti0 = state_params['ti0']
        ni = state_params['ni']
        ns = state_params['ns']

        print('instantiate PSFGibsonLanni')

        obj_psf = PSFGibsonLanni((sz, sy, sx), res_lateral, res_axial,
                                 numerical_aperture, lambda_,
                                 ti0, ni, ns)
        print('run PSFGibsonLanni')
        psf = obj_psf.run()

        self._out_data = {'data': psf, 'scale': (1, 1, 1),
                          'name': 'PSF Gibson-Lanni 3D'}

        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data['data'],
                              scale=self._out_data['scale'],
                              name=self._out_data['name'])
