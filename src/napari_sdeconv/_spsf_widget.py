"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from sdeconv.psfs.gaussian import metadata as gaussian_metadata
from sdeconv.psfs.gibson_lanni import metadata as gl_metadata
from sdeconv.psfs import SPSFGaussian, SPSFGibsonLanni

from ._framework import SNapariPlugin
from ._dict_widget import SDictWidget
from ._dict_worker import SDictWorker

if TYPE_CHECKING:
    import napari


# ################################################################################################ #
#                                    SGaussianPlugin
# ################################################################################################ #
class SGaussianPlugin(SNapariPlugin):
    def init_widget(self, napari_viewer):
        return SDictWidget(gaussian_metadata)

    def init_worker(self):
        return SDictWorker(gaussian_metadata)


# ################################################################################################ #
#                                    SGibsonLanniPlugin
# ################################################################################################ #
class SGibsonLanniPlugin(SNapariPlugin):
    def init_widget(self, napari_viewer):
        return SDictWidget(gl_metadata)

    def init_worker(self):
        return SDictWorker(gl_metadata)
