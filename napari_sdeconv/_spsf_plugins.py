from ._splugin import SNapariPlugin
from ._spsf_workers import (SPSFGaussian2DWorker, SPSFGaussian2DWidget,
                            SPSFGaussian3DWorker, SPSFGaussian3DWidget,
                            SPSFGibsonLanniWorker, SPSFGibsonLanniWidget)


class SPSFGaussian2D(SNapariPlugin):
    """Dock widget for generating a 2D Gaussian PSF image

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S PSF Gaussian 2D'
        self.widget = SPSFGaussian2DWidget(napari_viewer)
        self.worker = SPSFGaussian2DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()


class SPSFGaussian3D(SNapariPlugin):
    """Dock widget for generating a 2D Gaussian PSF image

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S PSF Gaussian 3D'
        self.widget = SPSFGaussian3DWidget(napari_viewer)
        self.worker = SPSFGaussian3DWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()


class SPSFGibsonLanni(SNapariPlugin):
    """Dock widget for generating a Gibson Lanni PSF image

    Parameters
    ----------
    napari_viewer: Viewer
        Napari viewer

    """
    def __init__(self, napari_viewer):
        super().__init__(napari_viewer)
        self.title = 'S PSF Gibson-Lanni'
        self.widget = SPSFGibsonLanniWidget(napari_viewer)
        self.worker = SPSFGibsonLanniWorker(napari_viewer, self.widget)
        self.widget.advanced.connect(self.set_advanced)
        self.init_ui()
