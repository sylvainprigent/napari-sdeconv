from ._splugin import SNapariPlugin
from ._srl_workers import (SRichardsonLucy2DWorker, SRichardsonLucy2DWidget,
                           SRichardsonLucy3DWorker, SRichardsonLucy3DWidget)


class SRichardsonLucy2D(SNapariPlugin):
    """Dock widget for 2D Richardson Lucy deconvolution

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S Richardson Lucy 2D'
        self.widget = SRichardsonLucy2DWidget(napari_viewer)
        self.worker = SRichardsonLucy2DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()


class SRichardsonLucy3D(SNapariPlugin):
    """Dock widget for 3D Richardson Lucy deconvolution

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S Richardson Lucy 3D'
        self.widget = SRichardsonLucy3DWidget(napari_viewer)
        self.worker = SRichardsonLucy3DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()
