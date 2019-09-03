# -*- coding: utf-8 -*-

#CREATION OF RVE_Geometry
import sys
import salome

#Create an instance of the study
salome.salome_init()
theStudy = salome.myStudy

#Adding to the path
import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/u1449908/Salome_files/AUTO_FIBER')

#Import the python script that generates the fiber coordinates
import hexagonal_mesh_noise

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

geompy = geomBuilder.New(theStudy)

#Making Geometry
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

#Creating the square face
geomObj = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sketch = geompy.Sketcher2D()
sketch.addPoint(0, 0)
sketch.addSegmentAbsolute(0, hexagonal_mesh_noise.a)
sketch.addSegmentAbsolute(hexagonal_mesh_noise.a, hexagonal_mesh_noise.a)
sketch.addSegmentAbsolute(hexagonal_mesh_noise.a, 0)
sketch.close()

Sketch = sketch.wire(geomObj)
Face = geompy.MakeFaceWires([Sketch], 1)
geompy.addToStudy( Sketch, 'Sketch' )
geompy.addToStudy( Face, 'Face' )

partition_tools = []
#adding the circles to be partitioned
for i in range(1, len(hexagonal_mesh_noise.coords)+1):
	Vertex = geompy.MakeVertex(hexagonal_mesh_noise.coords[i-1][0], hexagonal_mesh_noise.coords[i-1][1], 0)
	Circle = geompy.MakeCircle(Vertex, None, hexagonal_mesh_noise.d/2)
	geompy.addToStudy( Vertex, 'Vertex_'+ str(i) )
	geompy.addToStudy( Circle, 'Circle_'+ str(i) )
	partition_tools.append(Circle)

#partition the square with the fiber circles
Partition = geompy.MakePartition([Face], partition_tools, [], [], geompy.ShapeType["FACE"], 0, [], 0)
#Extrude the 2D sketch
Extrusion = geompy.MakePrismVecH(Partition, OZ, hexagonal_mesh_noise.a)
geompy.addToStudy( Extrusion, 'Extrusion' )

#trial
pmidle = geompy.MakeVertex(hexagonal_mesh_noise.d/4, 0, 0)
edge1 = geompy.GetEdgeNearPoint(Extrusion, pmidle)


geompy.ExportSTEP(Extrusion, "/home/u1449908/Salome_files/AUTO_FIBER/RVE.step", GEOM.LU_METER )

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
