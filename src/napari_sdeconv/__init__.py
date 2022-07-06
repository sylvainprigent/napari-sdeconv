__version__ = "1.0.0"
from ._sample_data import make_sample_data
from ._sdeconv_widget import SWienerPlugin, SRichardsonLucyPlugin, SpitfirePlugin

__all__ = (
    'SWienerPlugin',
    'SRichardsonLucyPlugin',
    'SpitfirePlugin'
)
