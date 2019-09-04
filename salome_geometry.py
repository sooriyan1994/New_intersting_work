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

###Making Geometry
#Creating the coordinate system
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

#Creating the square face from a sketch
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

partition_tools = [] #collects the circles which are used to partition the face
fiber_vertices = [] #collects the vertices of fibers

#adding the circles to be partitioned
for i in range(1, len(hexagonal_mesh_noise.coords)+1):
	Vertex = geompy.MakeVertex(hexagonal_mesh_noise.coords[i-1][0], hexagonal_mesh_noise.coords[i-1][1], 0)
	Circle = geompy.MakeCircle(Vertex, None, hexagonal_mesh_noise.d/2)
	#geompy.addToStudy( Vertex, 'Vertex_'+ str(i) ) #can be removed if we dont want it in the study
	#geompy.addToStudy( Circle, 'Circle_'+ str(i) ) #can be removed if we dont want it in the study
	partition_tools.append(Circle)
	fiber_vertices.append(Vertex)

#partitioning the square face with the fiber circles
Partition = geompy.MakePartition([Face], partition_tools, [], [], geompy.ShapeType["FACE"], 0, [], 0)
geompy.addToStudy( Partition, 'Partition' )
#Extrude the 2D sketch
Extrusion = geompy.MakePrismVecH(Partition, OZ, hexagonal_mesh_noise.a)
geompy.addToStudy( Extrusion, 'Extrusion' )

##Getting all vertices from the extruded RVE
back_O = geompy.GetVertexNearPoint(Extrusion, O)
back_OA = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(hexagonal_mesh_noise.a, 0, 0))
back_OB = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(0, hexagonal_mesh_noise.a, 0))
back_AB = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(hexagonal_mesh_noise.a, hexagonal_mesh_noise.a, 0))
front_1 = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(0, 0, hexagonal_mesh_noise.a))
front_2 = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(hexagonal_mesh_noise.a, 0, hexagonal_mesh_noise.a))
front_3 = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(hexagonal_mesh_noise.a, hexagonal_mesh_noise.a, hexagonal_mesh_noise.a))
front_4 = geompy.GetVertexNearPoint(Extrusion, geompy.MakeVertex(0, hexagonal_mesh_noise.a, hexagonal_mesh_noise.a))

geompy.addToStudyInFather(Extrusion, back_O, "Point on the back face (0, 0, 0)")
geompy.addToStudyInFather(Extrusion, back_OA, "Point on the back face (a, 0, 0)")
geompy.addToStudyInFather(Extrusion, back_OB, "point on the back face (0, a, 0)")
geompy.addToStudyInFather(Extrusion, back_AB, "point on the back face (a, a, 0)")
geompy.addToStudyInFather(Extrusion, front_1, "point on the front face (0, 0, a)")
geompy.addToStudyInFather(Extrusion, front_2, "point on the front face (a, 0, a)")
geompy.addToStudyInFather(Extrusion, front_3, "point on the front face (a, a, a)")
geompy.addToStudyInFather(Extrusion, front_4, "point on the front face (0, a, 0)")

##Getting all the edges
edge_front_top = geompy.GetEdge(Extrusion, front_3, front_4)
edge_front_right = geompy.GetEdge(Extrusion, front_2, front_3)
edge_front_bottom = geompy.GetEdge(Extrusion, front_1, front_2)
edge_front_left = geompy.GetEdge(Extrusion, front_1, front_4)
edge_top_left = geompy.GetEdge(Extrusion, front_4, back_OB)
edge_top_right = geompy.GetEdge(Extrusion, front_3, back_AB)
edge_bottom_right = geompy.GetEdge(Extrusion, front_2, back_OA)
edge_bottom_left = geompy.GetEdge(Extrusion, front_1, back_O)
edge_back_top = geompy.GetEdge(Extrusion, back_OB, back_AB)
edge_back_right = geompy.GetEdge(Extrusion, back_OA, back_AB)
#edge_back_bottom = geompy.GetEdge(Extrusion, back_O, back_OA)
edge_back_left = geompy.GetEdge(Extrusion, back_O, back_OB)
edge_back_bottom = geompy.GetEdgeNearPoint(Extrusion, geompy.MakeVertex(hexagonal_mesh_noise.a/2, 0, 0))

geompy.addToStudyInFather(Extrusion, edge_front_top, "Front top edge")
geompy.addToStudyInFather(Extrusion, edge_front_right, "Front right edge")
geompy.addToStudyInFather(Extrusion, edge_front_bottom, "Front bottom edge")
geompy.addToStudyInFather(Extrusion, edge_front_left, "Front left edge")
geompy.addToStudyInFather(Extrusion, edge_top_left, "Top left edge")
geompy.addToStudyInFather(Extrusion, edge_top_right, "Top right edge")
geompy.addToStudyInFather(Extrusion, edge_bottom_right, "Bottom right edge")
geompy.addToStudyInFather(Extrusion, edge_bottom_left, "Bottom left edge")
geompy.addToStudyInFather(Extrusion, edge_back_top, "Back top edge")
geompy.addToStudyInFather(Extrusion, edge_back_right, "Back right edge")
geompy.addToStudyInFather(Extrusion, edge_back_bottom, "Back bottom edge")
geompy.addToStudyInFather(Extrusion, edge_back_left, "Back left edge")


##Getting all the faces

Right_face = geompy.GetFaceByNormale( Extrusion, OX )
Left_face = geompy.GetFaceNearPoint( Extrusion, geompy.MakeVertex(0, hexagonal_mesh_noise.a/2, hexagonal_mesh_noise.a/2))
Front_face = geompy.GetFaceByNormale( Extrusion, OZ )
Back_face = geompy.GetFaceNearPoint( Extrusion, geompy.MakeVertex(hexagonal_mesh_noise.a/2, hexagonal_mesh_noise.a/2, 0))
Top_face = geompy.GetFaceByNormale( Extrusion, OY )
Bottom_face = geompy.GetFaceByPoints( Extrusion, back_O, back_OA, front_1, front_2)

geompy.addToStudyInFather(Extrusion, Right_face, "Right_face")
geompy.addToStudyInFather(Extrusion, Left_face, "Left_face")
geompy.addToStudyInFather(Extrusion, Front_face, "Front_face")
geompy.addToStudyInFather(Extrusion, Back_face, "Back_face")
geompy.addToStudyInFather(Extrusion, Top_face, "Top_face")
geompy.addToStudyInFather(Extrusion, Bottom_face, "Bottom_face")

##Getting the Volume 
Resin = geompy.GetBlockByParts(Extrusion, [Right_face, Left_face, Front_face, Back_face, Top_face, Bottom_face])
geompy.addToStudyInFather(Extrusion, Resin, "matrix")

	#Fiber = geompy.GetBlocksByParts(Extrusion, fiber_vertices)
	#for i in range(len(Fiber)):
	#	geompy.addToStudyInFather(Extrusion, Fiber[i], "Fiber "+str(i+1))
	#
	#del Fiber[0]

#getting the list of fibers
Fiber = []
for i in range(len(fiber_vertices)):
	Fiber.append(geompy.GetBlockNearPoint(Extrusion, fiber_vertices[i]))
	#geompy.addToStudyInFather(Extrusion, Fiber[i], "Fiber "+str(i+1)) 
	#Uncomment the above line if you need individual fibers to be in the study

#creating a group of list of fibers
Fibers = geompy.CreateGroup(Extrusion, geompy.ShapeType["SOLID"])
geompy.UnionList(Fibers, Fiber)
geompy.addToStudyInFather(Extrusion, Fibers, 'Fibers')

#Exporting the geometry into a .step file
geompy.ExportSTEP(Extrusion, "/home/u1449908/Salome_files/AUTO_FIBER/RVE.step", GEOM.LU_METER )

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
