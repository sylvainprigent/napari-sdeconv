# Description

`napari-sdeconv` is a suite of **Napari** plugins for the `sdeconv library
<https://sylvainprigent.github.io/sdeconv/>`_ dedicated to 2D and 3D images deconvolution. It contains multiple
deconvolution algorithms and PSF Generators.

* Example of deconvolution with Spitfire

![img](https://raw.githubusercontent.com/sylvainprigent/napari-sdeconv/main/docs/images/spitfire3D.png)


* Example of how to generate a 3D PSF

![img](https://raw.githubusercontent.com/sylvainprigent/napari-sdeconv/main/docs/images/gibson_lanni.png)


## Installation

You can install `napari-sdeconv` via [pip]:

    pip install napari-sdeconv
    

Note that the current version of the package on support python 3.9    

The deconvolution depends on FFTW c++ library. FFTW must be installed for the 
deconvolution plugin to work. The easiest method to install FFTW is to use 
conda:

    conda install -c conda-forge fftw

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [GNU GPL v3.0] license,
"napari-tracks-reader" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin
[file an issue]: https://github.com/sylvainprigent/napari-sdeconv/issues
[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
