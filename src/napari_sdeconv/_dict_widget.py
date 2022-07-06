import qtpy.QtCore
from qtpy.QtWidgets import (QWidget, QLabel, QGridLayout, QLineEdit, QGroupBox, QComboBox,
                            QVBoxLayout, QHBoxLayout, QSizePolicy, QCheckBox)
import napari
from ._framework import SNapariWidget


class SLayerImageWidget(SNapariWidget):
    def __init__(self, label, napari_viewer):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)
        self.label = label
        self.viewer = napari_viewer
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.layer_box = QComboBox()
        layout.addWidget(self.layer_box)
        self._on_layer_change(None)

    def _on_layer_change(self, e):
        """Update the plugin layers lists when napari layers are updated
        Parameters
        ----------
        e: QObject
            Qt event
        """
        self.layer_box.clear()
        for layer in self.viewer.layers:
            if isinstance(layer, napari.layers.image.image.Image):
                self.layer_box.addItem(layer.name)

    def state(self):
        return self.viewer.layers[self.layer_box.currentText()].data

    def check_inputs(self):
        if self.layer_box.count() == 0:
            self.show_error(f"The input {self.label} is empty !")
            return False
        return True


class SCoordinatesWidget(SNapariWidget):
    def __init__(self, label, data_type, default):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)
        self.data_type = data_type
        self.label = label
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(QLabel('x'))
        self.x_edit = QLineEdit(str(default[2]))
        layout.addWidget(self.x_edit)

        layout.addWidget(QLabel('y'))
        self.y_edit = QLineEdit(str(default[1]))
        layout.addWidget(self.y_edit)

        layout.addWidget(QLabel('z'))
        self.z_edit = QLineEdit(str(default[0]))
        layout.addWidget(self.z_edit)

    def state(self):
        if self.data_type == 'int':
            return int(self.z_edit.text()), int(self.y_edit.text()), int(self.x_edit.text())
        if self.data_type == 'float':
            return [float(self.z_edit.text()), float(self.y_edit.text()), float(self.x_edit.text())]

    def check_inputs(self):
        if self.data_type == 'float':
            try:
                _ = float(self.z_edit.text())
            except ValueError:
                self.show_error(f"Coordinate z for {self.label} must be a number")
                return False
            try:
                _ = float(self.y_edit.text())
            except ValueError:
                self.show_error(f"Coordinate y for {self.label} must be a number")
                return False
            try:
                _ = float(self.x_edit.text())
            except ValueError:
                self.show_error(f"Coordinate x for {self.label} must be a number")
                return False
        elif self.data_type == 'int':
            try:
                _ = int(self.z_edit.text())
            except ValueError:
                self.show_error(f"Coordinate z for {self.label} must be a integer")
                return False
            try:
                _ = int(self.y_edit.text())
            except ValueError:
                self.show_error(f"Coordinate y for {self.label} must be a integer")
                return False
            try:
                _ = int(self.x_edit.text())
            except ValueError:
                self.show_error(f"Coordinate x for {self.label} must be a integer")
                return False
        return True


class SLineWidget(SNapariWidget):
    def __init__(self, label, number_type, default_value):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)
        self.label = label
        self.data_type = number_type

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.edit = QLineEdit(str(default_value))
        layout.addWidget(self.edit, 0, qtpy.QtCore.Qt.AlignTop)
        self.setLayout(layout)

    def state(self):
        if self.data_type == 'int':
            return int(self.edit.text())
        if self.data_type == 'float':
            return float(self.edit.text())
        return self.edit.text()

    def check_inputs(self):
        if self.data_type == 'int':
            try:
                _ = int(self.edit.text())
            except ValueError:
                self.show_error(f"Value for {self.label} must be an integer")
                return False
        if self.data_type == 'float':
            try:
                _ = float(self.edit.text())
            except ValueError:
                self.show_error(f"Value for {self.label} must be a number")
                return False
        return True


class SBoolWidget(SNapariWidget):
    def __init__(self, label, default):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.combobox = QComboBox()
        self.combobox.addItems(('True', 'False'))
        if default == 'False':
            self.combobox.setCurrentIndex(1)
        layout.addWidget(self.combobox)
        self.setLayout(layout)

    def state(self):
        if self.combobox.currentText() == 'True':
            return True
        return False

    def check_inputs(self):
        return True


class SDictWidget(SNapariWidget):
    """Create a parameters widget from a dictionary
    Parameters
    ----------
    params: dict
        Dictionary describing the parameters
    """
    def __init__(self, params, napari_viewer=None):
        super().__init__()
        self.metadata = params
        self.viewer = napari_viewer
        self.params = {}
        self.layout = QGridLayout()
        self.layout.setContentsMargins(3, 11, 3, 11)
        self.setLayout(self.layout)
        self._line_idx = 0
        self._image_layers = []
        self._widgets = []

        # advanced button
        advanced_box = QCheckBox('Advanced')
        advanced_box.stateChanged.connect(self.toggle_advanced)
        self.layout.addWidget(advanced_box, 0, 0, 1, 2)
        self._line_idx += 1

        # widgets
        for key, value in params['inputs'].items():
            if value['type'] == 'Image':
                self.add_layer_image(key, value)
            elif 'zyx' in value['type']:
                self.add_coordinates(key, value)
            elif value['type'] == 'float':
                self.add_float(key, value)
            elif value['type'] == 'int':
                self.add_int(key, value)
            elif value['type'] == 'bool':
                self.add_bool(key, value)
            elif value['type'] == 'select':
                self.add_select_edit(key, value)
            else:
                self.add_line_edit(key, value)
        # hide empty widget
        if len(params['inputs']) == 0:
            self.setFixedHeight(0)

        self.layout.addWidget(QWidget(), self._line_idx, 0)
        self.toggle_advanced(False)

    def toggle_advanced(self, is_advanced):
        for widget in self._widgets:
            if widget['widget'].is_advanced:
                widget['label'].setVisible(is_advanced)
                widget['widget'].setVisible(is_advanced)

    def _register_widget(self, label, widget, metadata):
        if 'advanced' in metadata:
            widget.is_advanced = metadata['advanced']
        self._widgets.append({'label': label, 'widget': widget})

    def add_layer_image(self, key, metadata):
        """Add a combobox to select an image layer

        Parameters
        ----------
        key: str
            ID of the parameter
        metadata: dict
            metadata of the widget

        """
        label = QLabel(metadata['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        widget = SLayerImageWidget(metadata['label'], self.viewer)
        self._image_layers.append(widget)
        self.layout.addWidget(widget, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': metadata['type'],
            'label': metadata['label'],
            'help': metadata['help'],
            'widget': widget
        }
        self._register_widget(label, widget, metadata)

    def add_coordinates(self, key, metadata):
        """Add a coordinate (z, y, x) input widget

        Parameters
        ----------
        key: str
            ID of the parameter
        metadata: dict
            metadata of the widget

        """
        data_type = 'float'
        if 'int' in metadata['type']:
            data_type = 'int'
        widget = SCoordinatesWidget(metadata['label'], data_type, metadata['default'])
        label = QLabel(metadata['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        self.layout.addWidget(widget, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': metadata['type'],
            'label': metadata['label'],
            'help': metadata['help'],
            'default': metadata['default'],
            'range': None,
            'widget': widget
        }
        self._register_widget(label, widget, metadata)

    def add_select_edit(self, key, value):
        print('add select with dict=', value)
        label = QLabel(value['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        select_edit = QComboBox()
        select_edit.addItems([str(x) for x in value['values']])
        select_edit.setCurrentText(str(value['default']))
        self.layout.addWidget(select_edit, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': value['type'],
            'label': value['label'],
            'help': value['help'],
            'default': value['default'],
            'range': None,
            'widget': select_edit
        }
        self._register_widget(label, select_edit, value)

    def add_float(self, key, metadata):
        """Add a float input widget

        Parameters
        ----------
        key: str
            ID of the parameter
        metadata: dict
            metadata of the widget

        """
        widget = SLineWidget(metadata['label'], 'float', metadata['default'])
        label = QLabel(metadata['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        self.layout.addWidget(widget, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': metadata['type'],
            'label': metadata['label'],
            'help': metadata['help'],
            'default': metadata['default'],
            'range': None,
            'widget': widget
        }
        self._register_widget(label, widget, metadata)

    def add_int(self, key, metadata):
        """Add a integer input widget

        Parameters
        ----------
        key: str
            ID of the parameter
        metadata: dict
            metadata of the widget

        """
        widget = SLineWidget(metadata['label'], 'int', metadata['default'])
        label = QLabel(metadata['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        self.layout.addWidget(widget, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': metadata['type'],
            'label': metadata['label'],
            'help': metadata['help'],
            'default': metadata['default'],
            'range': None,
            'widget': widget
        }
        self._register_widget(label, widget, metadata)

    def add_line_edit(self, key, metadata):
        widget = SLineWidget(metadata['label'], 'str', metadata['default'])
        label = QLabel(metadata['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        self.layout.addWidget(widget, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': metadata['type'],
            'label': metadata['label'],
            'help': metadata['help'],
            'default': metadata['default'],
            'range': None,
            'widget': widget
        }
        self._register_widget(label, widget, metadata)

    def add_bool(self, key, metadata):
        widget = SBoolWidget(metadata['label'], metadata['default'])
        label = QLabel(metadata['label'])
        self.layout.addWidget(label, self._line_idx, 0)
        self.layout.addWidget(widget, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': metadata['type'],
            'label': metadata['label'],
            'help': metadata['help'],
            'default': metadata['default'],
            'range': None,
            'widget': widget
        }
        self._register_widget(label, widget, metadata)

    def check_inputs(self):
        for key, value in self.params.items():
            if not value['widget'].check_inputs():
                return False
        return True

    def state(self):
        """read the parameters from the widget
        Returns
        -------
        dict of parameters values
        """
        params = self.metadata.copy()
        params['inputs'] = {}
        if 'outputs' not in params:
            params['outputs'] = []
        for key, value in self.params.items():
            params['inputs'][key] = value['widget'].state()
        print('dict widget state=', params)
        return params
