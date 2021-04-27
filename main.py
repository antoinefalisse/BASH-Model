# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:00:09 2021

@author: u0101727
"""

import os
import numpy as np
import pickle

# %% User inputs

'''
Select camera:
    '0': front
    '1': 45deg clockwise
    '2': 90deg clockwise
    '3': 135deg clockwise
    '4': 180deg clockwise (back)
    '5': 225deg clockwise
    '6': 270deg clockwise
    '7': 315deg clockwise
'''
cameras = [str(i) for i in range(8)]
# remove laterla cameras
cameras.remove('2')
cameras.remove('6')

'''
Select distance (m)
'''
distance = '4'

# %% Paths

pathBase = os.getcwd()
pathData = os.path.join(pathBase, 'data')
pathOsim = os.path.join(pathData, 'OSIM')
pathExe = os.path.join(pathBase, 'build', 'x64', 'Release', 'SCAPE.exe')

osimModelName = 'subject3_c33_new.osim'
pathOsimModel = os.path.join(pathOsim, osimModelName)

motFileName = 'IK_c33_99.mot'
pathMotFile = os.path.join(pathOsim, motFileName)

pathVideos = os.path.join(pathData, 'Videos')
pathVideosDataset = os.path.join(pathVideos, 'DatasetTest')
pathVideosSubject = os.path.join(pathVideosDataset, 'SubjectTest')
pathVideosTrial = os.path.join(pathVideosSubject, 'TrialTest')

# loop over camera
for camera in cameras:

    pathVideosCam = os.path.join(pathVideosSubject, 'Cam{}'.format(camera), "InputMedia", "tesTrial")
    if not os.path.exists(pathVideosCam):
        os.makedirs(pathVideosCam)
        
    baseModelDir = os.path.join(pathData, 'baselineModel/')
    
    # %% Generate images
    command = "{} --osim {} --mot {} --model {} --output {} --camera {} --distance {}".format(
        pathExe, pathOsimModel, pathMotFile, baseModelDir, pathVideosCam, camera, distance)
    os.system(command)
    
    # %% Create video from images
    # Extract framerate from mot file - we should have one image per frame.
    from utils import storage2numpy
    motion = storage2numpy(pathMotFile)
    time = motion['time']
    framerate_in = int(np.round(1/np.mean(np.diff(time))))
    # Fix output framerate to 60 Hz.
    framerate_out = 60
    
    # We start from image #2, since the first 2 are before presentation mode.
    commande_ffmpeg = "ffmpeg -framerate {} -start_number 2 -i {}/image%d.png -c:v libx264 -r {} -pix_fmt yuv420p {}/output.mp4".format(
        framerate_in, pathVideosCam, framerate_out, pathVideosCam)
    os.system(commande_ffmpeg)
    
    # %% Retrieve camera matrix
    cameraParams = {}
    
    # Intrinsics
    intrinsicsFile = open("{}/parameters4Intrinsics.txt".format(pathVideosCam), "r")
    intrinsics_str = intrinsicsFile.readlines()
    fov_deg = float(intrinsics_str[0][:-1])
    width = float(intrinsics_str[1][:-1])
    height  = float(intrinsics_str[2][:-1])
    fov_rad = fov_deg*np.pi/180
    f = 0.5 * height / np.tan(fov_rad/2) #cf http://paulbourke.net/miscellaneous/lens/  (NOTE: focal length is in pixels)
    
    # TODO: to confirm
    cx = width/2
    cy = height/2
    intrinsics = np.array([
    [f, 0, cx],
    [0., f, cy],
    [0.,0.,1.]
    ], dtype=np.float64)
    cameraParams['intrinsicMat'] = intrinsics
    
    # Extrinsics
    extrinsicsFile = open("{}/parameters4Extrinsics.txt".format(pathVideosCam), "r")
    extrinsics_str = extrinsicsFile.readlines()
    
    R = np.zeros((3,3))
    # Rotation
    for i in range(3):
        row = extrinsics_str[i].split(" ")    
        for j, elm in enumerate(row):
            if j < 3:
                R[i,j] = float(elm)
    cameraParams['rotation'] = R
    # Translation
    t = np.zeros((3,1))
    row = extrinsics_str[3].split(" ")  
    for j, elm in enumerate(row):
            if j < 3:
                t[j,0] = float(elm)
    cameraParams['translation'] = t
    
    open_file = open("{}/cameraIntrinsicsExtrinsics.pickle".format(pathVideosCam), "wb")
    pickle.dump(cameraParams, open_file)
    open_file.close()
