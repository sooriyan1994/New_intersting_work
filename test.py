import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/u1449908/Salome_files/AUTO_FIBER')

import trial

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
Face_1 = geompy.MakeFaceHW(trial.a, trial.a, 1)
geompy.addToStudy( Face_1, 'Face_1' )

partition_tools = []

for i in range(1, len(trial.coord)+1):
	Vertex = geompy.MakeVertex(trial.coord[i-1][0], trial.coord[i-1][1], 0)
	Circle = geompy.MakeCircle(Vertex, None, 1)
	print(type(Circle))
	geompy.addToStudy( Vertex, 'Vertex_'+ str(i) )
	geompy.addToStudy( Circle, 'Circle_'+ str(i) )
	partition_tools.append('Circle_'+ str(i))

Partition_1 = geompy.MakePartition([Face_1], partition_tools, [], [], geompy.ShapeType["FACE"], 0, [], 0)
#Partition_1 = geompy.MakePartition([Face_1], [Circle_3, Circle_4, Circle_5, Circle_6, Circle_7, Circle_8], [], [], geompy.ShapeType["FACE"], 0, [], 0)
Extrusion_1 = geompy.MakePrismVecH(Partition_1, OZ, 20)
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
