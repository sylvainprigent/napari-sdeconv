"""Framework designed to create napari plugins recording the widget state

Classes
-------
SNapariWidget
SNapariWorker
SLogWidget
SProgressObserver


"""
from qtpy.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton,
                            QHBoxLayout, QVBoxLayout, QProgressBar,
                            QTextEdit, QMessageBox)
from qtpy.QtCore import Signal, QThread, QObject


class SNapariWidget(QWidget):
    """Interface for a napari widget with state
    This interface implements three methods
    - show_error: to display a user input error
    - check_inputs (abstract): to check all the user input from the plugin widget
    - state (abstract): to get the plugin widget state, ie the user inputs values set in the widget
    """
    advanced = Signal(bool)
    enable = Signal(bool)

    def __init__(self, napari_viewer=None):
        super().__init__()
        self.viewer = napari_viewer
        self.is_advanced = False

    @staticmethod
    def show_error(message):
        """Display an error message in a QMessage box
        Parameters
        ----------
        message: str
            Error message
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setText(message)
        msg.setWindowTitle("STracking error")
        msg.exec_()

    def check_inputs(self):
        """Check the user input in this widget
        Returns:
            True if no error, False if at least one input contains an error.
            (ex not well writen number)
        """
        raise NotImplementedError()

    def state(self):
        """Return the current state of the widget
        The state in inputs values displayed in the the widget. Example
        .. highlight:: python
        .. code-block:: python
            {'name': 'SDoGDetector',
             'inputs': {'image': self._input_layer_box.currentText()},
                        'min_sigma': float(self._min_sigma_value.text()),
                        'max_sigma': float(self._max_sigma_value.text()),
                         'threshold': float(self._threshold_value.text()),
                         'sigma_ratio': float(self._sigma_ratio_value.text()),
                         'overlap': float(self._overlap_value.text()),
                         'current_frame': self._current_frame_check.isChecked()
                            },
             'outputs': ['points', 'DoG detections']
             }
        Returns:
            dict: a dictionary containing the widget inputs
        """
        raise NotImplementedError()


class SNapariWorker(QObject):
    """Interface for a napari plugin worker
    The worker is an object that run the calculation (run method) using the inputs
    from the plugin widget interface (SNapariWidget state)
    """
    finished = Signal()
    progress = Signal(int)
    log = Signal(str)

    def __init__(self):
        super().__init__()
        self._state = None
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def state(self):
        """Get the states from the SNapariWidget"""
        return self._state

    def set_state(self, state_dict):
        self._state = state_dict

    def run(self):
        """Exec the data processing"""
        raise NotImplementedError()


class SLogWidget(QWidget):
    """Widget to log the STracking plugins messages in the graphical interface"""
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = QProgressBar()
        self.log_area = QTextEdit()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_area)
        self.setLayout(layout)

    def set_advanced(self, mode: bool):
        """Show hide the log area depending on the plugin mode"""
        if mode:
            self.log_area.setVisible(True)
        else:
            self.log_area.setVisible(False)

    def set_progress(self, value: int):
        """Callback to update the progress bar"""
        self.progress_bar.setValue(value)

    def add_log(self, value: str):
        """Callback to add a new message in the log area"""
        self.log_area.append(value)

    def clear_log(self):
        """Callback to clear all the log area"""
        self.log_area.clear()


class SProgressObserver(QObject):
    """Implement the observer design pattern to display tools progress"""
    progress_signal = Signal(int)
    notify_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def progress(self, value):
        """Callback to refresh the computation progress"""
        self.progress_signal.emit(value)

    def notify(self, message):
        """Callback to notify a new log message"""
        self.notify_signal.emit(message)


class SNapariPlugin(QWidget):
    """Interface for a SNapariPlugin
       This is a generic interface for a recordable napari plugin using a worker

    Parameters
    ----------
    napari_viewer: QWidget
        Instance of the napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.thread = QThread()
        self._worker = None
        self._observer = SProgressObserver()

        # init the widget
        self._widget = self.init_widget(self.viewer)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self._widget, 0, 0, 1, 2)

        # init the worker
        self._worker = self.init_worker()
        self._worker.moveToThread(self.thread)
        self.thread.started.connect(self._worker.run)
        self._worker.finished.connect(self.thread.quit)
        self._worker.finished.connect(self.set_outputs)
        self._observer.progress_signal.connect(self._on_progress)
        self._worker.add_observer(self._observer)

        # add the run area
        self.run_btn = QPushButton("Run")
        self.layout().addWidget(self.run_btn, 1, 0, 1, 2)
        self.run_btn.clicked.connect(self._on_click_run)

        self.progress_bar = QProgressBar()
        self.layout().addWidget(self.progress_bar, 2, 0, 1, 2)
        self.layout().addWidget(QWidget(), 3, 0, 1, 2)

    def state(self):
        return self._widget.state()

    def init_widget(self, napari_viewer):
        """Initialize the widget
        This widget must be a SNapariWidget to be recordable

        Parameters
        ----------
        napari_viewer: QWidget
            Instance of the napari viewer

        Returns
        -------
        a SNapariWidget widget

        """
        raise NotImplementedError()

    def init_worker(self):
        """Initialize the worker
        The worker must be a SNapariWorker

        Returns
        -------
        the plugin worker using the SNapariWorker interface

        """
        raise NotImplementedError()

    def set_outputs(self):
        for key in self._worker.state()['outputs'].keys():
            output = self._worker.state()['outputs'][key]
            if output['type'] == 'Image':
                self.viewer.add_image(output['data'], name=output['label'])
        self.progress_bar.setValue(100)

    def _on_click_run(self):
        self.progress_bar.setValue(0)
        if self._widget.check_inputs():
            self._worker.set_state(self._widget.state())
            self.thread.start()

    def _on_progress(self, value):
        self.progress_bar.setValue(value)
