"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_plugin_engine import napari_hook_implementation
from ._spitfire_plugins import Spitfire2D, Spitfire3D
from ._srl_plugins import SRichardsonLucy2D, SRichardsonLucy3D
from ._swiener_plugins import SWiener2D, SWiener3D
from ._spsf_plugins import SPSFGaussian2D, SPSFGibsonLanni


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [Spitfire2D,
            Spitfire3D,
            SRichardsonLucy2D,
            SRichardsonLucy3D,
            SWiener2D,
            SWiener3D,
            SPSFGaussian2D,
            SPSFGibsonLanni]
