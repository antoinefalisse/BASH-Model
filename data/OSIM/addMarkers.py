# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 18:29:23 2021

@author: u0101727
"""

import os
import opensim
import numpy as np

pathMain = os.getcwd()

modelName = "subject3_c33"
referenceModelName = "runMaD_Scaled"
pathReferenceModel = os.path.join(pathMain, referenceModelName + ".osim")
pathMyModel = os.path.join(pathMain, modelName + ".osim")


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
    
    # # diff in scale factors
    ratio_scale_factors = c_scale_factors / my_scale_factors
    
    # ratio_scale_factors = np.array([1.25200731, 1.25200731, 1.25200731])
    
    # scaled location
    my_marker_location = c_marker_location / ratio_scale_factors
    # my_marker_location = np.array([ 0.        , -0.01597435, -0.02396152])
    
    newMkr = opensim.Marker()
    newMkr.setName(c_marker.getName())
    newMkr.setParentFrameName("/bodyset/{}".format(myBody.getName()))
    newMkr.set_location(opensim.Vec3(my_marker_location))
    myModel.addMarker(newMkr)
    
myModel.finalizeConnections
myModel.initSystem()
pathNewModel = os.path.join(pathMain, modelName + "_new.osim")
myModel.printToXML(pathNewModel)
