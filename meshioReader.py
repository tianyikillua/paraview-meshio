import meshio
import numpy as np

from paraview.util.vtkAlgorithm import smproperty, smproxy, smdomain, smhint
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


__author__ = "Tianyi Li"
__email__ = "tianyikillua@gmail.com"
__copyright__ = "Copyright (c) 2019 {} <{}>".format(__author__, __email__)
__license__ = "License :: OSI Approved :: MIT License"
__version__ = "0.0.1"
__status__ = "Development Status :: 4 - Beta"


meshio_to_vtk_type = meshio._vtk.meshio_to_vtk_type
meshio_supported_ext = [
    ext[1:] for ext in meshio._helpers._extension_to_filetype.keys()
]


@smproxy.reader(
    label="meshio Reader",
    extensions=meshio_supported_ext,
    file_description="meshio-supported files",
)
class meshioReader(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(
            self, nInputPorts=0, nOutputPorts=1, outputType="vtkUnstructuredGrid"
        )
        self._filename = None

    @smproperty.stringvector(name="FileName")
    @smdomain.filelist()
    @smhint.filechooser(
        extensions=meshio_supported_ext, file_description="meshio-supported files"
    )
    def SetFileName(self, name):
        if self._filename != name:
            self._filename = name
            self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        output = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfo))

        # Use meshio to read the mesh
        mesh = meshio.read(self._filename)
        points, cells = mesh.points, mesh.cells

        # Nodes
        if points.shape[1] == 2:
            points = np.hstack([points, np.zeros((len(points), 1))])
        output.SetPoints(points)

        # Elements, adapted from
        # https://github.com/nschloe/meshio/blob/master/test/legacy_writer.py
        cell_types = np.array([], dtype=np.ubyte)
        cell_offsets = np.array([], dtype=int)
        cell_conn = np.array([], dtype=int)
        for meshio_type in cells:
            vtk_type = meshio_to_vtk_type[meshio_type]
            ncells, npoints = cells[meshio_type].shape
            cell_types = np.hstack(
                [cell_types, np.full(ncells, vtk_type, dtype=np.ubyte)]
            )
            conn = np.hstack(
                [npoints * np.ones((ncells, 1), dtype=int), cells[meshio_type]]
            ).flatten()
            cell_conn = np.hstack([cell_conn, conn])
            offsets = len(cell_offsets) + (1 + npoints) * np.arange(ncells, dtype=int)
            cell_offsets = np.hstack([cell_offsets, offsets])
        output.SetCells(cell_types, cell_offsets, cell_conn)

        # Point data
        for name, array in mesh.point_data.items():
            output.PointData.append(array, name)

        # Cell data
        def celldata_array(name):
            array = None
            for celltype in mesh.cells:
                values = mesh.cell_data[celltype][name]
                if array is None:
                    array = values
                else:
                    array = np.concatenate([array, values])
            return array

        celldata_names = [
            set(cell_data.keys()) for cell_data in mesh.cell_data.values()
        ]
        celldata_names = (
            set.intersection(*celldata_names) if len(celldata_names) > 0 else []
        )
        for name in celldata_names:
            array = celldata_array(name)
            output.CellData.append(array, name)

        return 1
