"""
This script adds markers to the scaled model, so that it can be used by BASH.
The baseline model of BASH contains specific markers that need to be part of 
the OpenSim model so that the BASH model can be scaled based on the dimensions
of the OpenSim model. Here, we add markers to the OpenSim model using as
reference the OpenSim model 'provided' with BASH. We extract the position of
the markers as well as the scaling factors of the corresponding segments and
add the markers to the OpenSim model while scaling their positions
accordingly.

@author: Antoine Falisse
"""

import os
import opensim

pathMain = os.getcwd()
pathOSIM = os.path.join(pathMain, 'data', 'OSIM')

modelName = "testModel"
referenceModelName = "referenceScaledModel"
pathReferenceModel = os.path.join(pathOSIM, referenceModelName + ".osim")
pathMyModel = os.path.join(pathOSIM, modelName + ".osim")


referenceModel = opensim.Model(pathReferenceModel)   
referenceModel.initSystem()
markerSet = referenceModel.get_MarkerSet()

myModel = opensim.Model(pathMyModel)
myModel.initSystem()
myBodySet = myModel.get_BodySet()

for c_idx in range(markerSet.getSize()):
    
    # reference model
    c_marker = markerSet.get(c_idx)
    c_marker_parentFrame = c_marker.getParentFrame()
    c_marker_location = c_marker.get_location().to_numpy()  
    c_attached_geometry = c_marker_parentFrame.get_attached_geometry(0)
    c_scale_factors = c_attached_geometry.get_scale_factors().to_numpy()
    
    # my model
    myBody = myBodySet.get(c_marker_parentFrame.getName())
    my_attached_geometry = myBody.get_attached_geometry(0)
    my_scale_factors = my_attached_geometry.get_scale_factors().to_numpy()
    
    # diff in scale factors
    ratio_scale_factors = c_scale_factors / my_scale_factors
    
    # scaled location
    my_marker_location = c_marker_location / ratio_scale_factors
    
    newMkr = opensim.Marker()
    newMkr.setName(c_marker.getName())
    newMkr.setParentFrameName("/bodyset/{}".format(myBody.getName()))
    newMkr.set_location(opensim.Vec3(my_marker_location))
    myModel.addMarker(newMkr)
    
myModel.finalizeConnections
myModel.initSystem()
pathNewModel = os.path.join(pathOSIM, modelName + "_markersBASH.osim")
myModel.printToXML(pathNewModel)
