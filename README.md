# napari-sdeconv

[![License](https://img.shields.io/pypi/l/napari-sdeconv.svg?color=green)](https://github.com/sylvainprigent/napari-sdeconv/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-sdeconv.svg?color=green)](https://pypi.org/project/napari-sdeconv)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-sdeconv.svg?color=green)](https://python.org)
[![tests](https://github.com/sylvainprigent/napari-sdeconv/workflows/tests/badge.svg)](https://github.com/sylvainprigent/napari-sdeconv/actions)
[![codecov](https://codecov.io/gh/sylvainprigent/napari-sdeconv/branch/master/graph/badge.svg)](https://codecov.io/gh/sylvainprigent/napari-sdeconv)

2D and 3D image deconvolution plugins. Available methods are:
- Wiener (2D and 3D)
- Richardson-Lucy (2D and 3D)
- Spitfire - hessian sparse regularized deconvolution (2D and 3D)

Available plugins to create PSFs are:
- PSF Gaussian (2D)
- PSF Gibson-Lanni (3D)

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using with [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/docs/plugins/index.html
-->

## Installation

You can install `napari-sdeconv` via [pip]:

    pip install napari-sdeconv
    

The deconvolution depends on FFTW c++ library. FFTW must be installed for the 
deconvolution plugin to work. The easiest method to install FFTW is to use 
conda:

    conda install -c conda-forge fftw
        

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [GNU GPL v3.0] license,
"napari-sdeconv" is free and open source software

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
