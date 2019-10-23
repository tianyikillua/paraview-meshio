# ParaView `meshio` Reader

This repository contains a ParaView Python plugin (`meshioReader.py`) that can be loaded by ParaView to read all the mesh formats supported by the [meshio](https://github.com/nschloe/meshio) library.

### Installation

1. Download the `meshio` library and put the `meshio` folder into the `site-packages` directory of ParaView. For instance, under Windows, it is `bin\Lib\site-packages`. You need to make sure that ParaView uses a Python version that supports `meshio`, that is at least Python 3.
2. Download `meshioReader.py` and load the plugin under ParaView, via *Tools* / *Manage Plugins* / *Load New*. You can optionally check the option *Auto Load*.
3. That's it. You can now load *almost* all `meshio`-supported mesh formats.

In order that `meshio` can indeed read all the supported formats, it need several other libraries: `lxml`, `h5py` and `netCDF4`. For the first two, you can simply proceed like `meshio` and copy the `lxml`, `h5py` folders into the `site-packages` directory. For `netCDF4` more investigations are needed.

### Usage

When opening the file, `meshio`-supported mesh formats are now [automatically available](https://user-images.githubusercontent.com/4027283/67407097-4a8bb180-f5b7-11e9-82b7-13480f76aa4a.png). This means you can now load those that can not be read by ParaView alone
- Gmsh (.msh), so you do not need to compile the [GmshReader](https://github.com/Kitware/ParaView/tree/master/Plugins/GmshReader`) plugin
- Abaqus (.inp)
- Nastran (.nas, .fem)
- DOLFIN (.xml)
- and others...

If point data or cell data are defined in the mesh file, that they will be also available in ParaView. [For instance](https://user-images.githubusercontent.com/4027283/67407675-27adcd00-f5b8-11e9-91e9-1d37d31cd23f.png) the `gmsh:physical` cell data for sub-region definitions.


### License

`meshioReader.py` is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
