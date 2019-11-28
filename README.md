# ParaView `meshio` Reader / Writer

This repository contains a ParaView Python plugin (`meshioPlugin.py`) that can be loaded by ParaView to read and write all the mesh formats supported by the [meshio](https://github.com/nschloe/meshio) library.

## Installation and updates

If you have downloaded a binary version of ParaView, you may proceed as follows
1. Download the `meshio` library and put the `meshio` folder into the `site-packages` directory of ParaView. For instance, under Windows, it is `bin\Lib\site-packages`. You need to make sure that ParaView uses a Python version that supports `meshio`, that is at least Python 3.
2. Download `meshioPlugin.py` and load the plugin under ParaView, via *Tools* / *Manage Plugins* / *Load New*. You can optionally check the option *Auto Load*.
3. That's it. You can now load and save *almost* all `meshio`-supported mesh formats.

In order that `meshio` can indeed read all the supported formats, it need several other libraries: `lxml`, `h5py` and `netCDF4`. You can simply proceed like `meshio` and copy the `lxml`, `h5py` and `netCDF4` folders from your own Python environment into the `site-packages` directory.

To ensure that the current plugin is up to date, you may clone this repository and frequently pull the latest updates
``` sh
git clone https://github.com/tianyikillua/paraview-meshio.git
git pull
```

## Usage

When opening the file, `meshio`-supported mesh formats are now automatically available through the *Open* dialog. This means you can now load those that can not be read by ParaView alone
- Gmsh (.msh), so you no longer need the [GmshReader](https://github.com/Kitware/ParaView/tree/master/Plugins/GmshReader) plugin
- Abaqus (.inp)
- Nastran (.nas, .fem)
- DOLFIN (.xml)
- and others...see [meshio](https://github.com/nschloe/meshio)

If point data, cell data and field data are defined in the mesh file, they will be also available in ParaView.

You can also now use the *Save Data* dialog to convert the current unstructured mesh to another `meshio`-supported mesh format.

## License

`meshioPlugin.py` is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
