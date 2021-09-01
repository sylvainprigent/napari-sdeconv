from ._splugin import SNapariPlugin
from ._spitfire_workers import (Spitfire2DWorker, Spitfire2DWidget,
                                Spitfire3DWorker, Spitfire3DWidget)


class Spitfire2D(SNapariPlugin):
    """Dock widget for 2D spitfire deconvolution

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'Spitfire 2D'
        self.widget = Spitfire2DWidget(napari_viewer)
        self.worker = Spitfire2DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()


class Spitfire3D(SNapariPlugin):
    """Dock widget for 3D spitfire deconvolution

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'Spitfire 3D'
        self.widget = Spitfire3DWidget(napari_viewer)
        self.worker = Spitfire3DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()
