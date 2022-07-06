"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from sdeconv.deconv.wiener import metadata as wiener_metadata
from sdeconv.deconv.richardson_lucy import metadata as rl_metadata
from sdeconv.deconv.spitfire import metadata as spitfire_metadata
from sdeconv.deconv.wiener import swiener
from sdeconv.deconv.richardson_lucy import srichardsonlucy
from sdeconv.deconv.spitfire import spitfire
from ._framework import SNapariPlugin
from ._dict_widget import SDictWidget
from ._dict_worker import SDictWorker

if TYPE_CHECKING:
    import napari


# ################################################################################################ #
#                                    SWienerPlugin
# ################################################################################################ #
class SWienerPlugin(SNapariPlugin):
    def init_widget(self, napari_viewer):
        return SDictWidget(wiener_metadata, napari_viewer)

    def init_worker(self):
        return SDictWorker(wiener_metadata)


# ################################################################################################ #
#                                 SRichardsonLucyPlugin
# ################################################################################################ #
class SRichardsonLucyPlugin(SNapariPlugin):
    def init_widget(self, napari_viewer):
        return SDictWidget(rl_metadata, napari_viewer)

    def init_worker(self):
        return SDictWorker(rl_metadata)


# ################################################################################################ #
#                                 SSpitfirePlugin
# ################################################################################################ #
class SpitfirePlugin(SNapariPlugin):
    def init_widget(self, napari_viewer):
        return SDictWidget(spitfire_metadata, napari_viewer)

    def init_worker(self):
        return SDictWorker(spitfire_metadata)
