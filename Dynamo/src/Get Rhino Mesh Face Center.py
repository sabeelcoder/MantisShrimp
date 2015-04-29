#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
clr.AddReference('ProtoGeometry')

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os
appDataPath = os.getenv('APPDATA')
msPath = appDataPath + r"\Dynamo\0.8\packages\Mantis Shrimp\extra"
rhPath = appDataPath + r"\Dynamo\0.8\packages\Mantis Shrimp\bin"
rhDllPath = appDataPath + r"\Dynamo\0.8\packages\Mantis Shrimp\bin\Rhino3dmIO.dll"
if msPath not in sys.path:
	sys.path.Add(msPath)
if rhPath not in sys.path:
	sys.path.Add(rhPath)
	clr.AddReferenceToFileAndPath(rhDllPath)

from Autodesk.DesignScript.Geometry import *
import Rhino as rc

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
rhObjects = IN[0]

#3dPoint Conversion function
def rhPoint3dToPoint(rhPoint):
	rhPointX = rhPoint.X
	rhPointY = rhPoint.Y
	rhPointZ = rhPoint.Z
	return Point.ByCoordinates(rhPointX, rhPointY, rhPointZ)

#convert rhino/gh geometry to ds geometry
points = [[] for i in range(len(rhObjects))]
for index, item in enumerate(rhObjects):
	try:
		item = item.Geometry
	except:
		pass
	if item.ToString() == "Rhino.Geometry.Mesh":
		faces = item.Faces
		for i in range(0, faces.Count, 1):
			points[index].append(rhPoint3dToPoint(faces.GetFaceCenter(i)))
	else:
		message = "Please provide Mesh to extract \nFace Center points."

#Assign your output to the OUT variable
if len(points) == 0:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
else:
	OUT = points
