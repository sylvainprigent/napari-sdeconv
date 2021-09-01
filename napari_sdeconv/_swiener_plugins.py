from ._splugin import SNapariPlugin
from ._swiener_workers import (SWiener2DWorker, SWiener2DWidget,
                               SWiener3DWorker, SWiener3DWidget)


class SWiener2D(SNapariPlugin):
    """Dock widget for 2D Wiener deconvolution

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S Wiener 2D'
        self.widget = SWiener2DWidget(napari_viewer)
        self.worker = SWiener2DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()


class SWiener3D(SNapariPlugin):
    """Dock widget for 3D Wiener deconvolution

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S Wiener 3D'
        self.widget = SWiener3DWidget(napari_viewer)
        self.worker = SWiener3DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()
