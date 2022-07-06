import numpy as np

from napari_sdeconv import SWienerPlugin, SRichardsonLucyPlugin, SpitfirePlugin


def test_wiener_widget(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)))

    # create our widget, passing in the viewer
    my_widget = SWienerPlugin(viewer)

    return True


def test_richardson_lucy_widget(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)))

    # create our widget, passing in the viewer
    my_widget = SRichardsonLucyPlugin(viewer)

    return True


def test_spitfire_widget(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)))

    # create our widget, passing in the viewer
    my_widget = SpitfirePlugin(viewer)

    return True
