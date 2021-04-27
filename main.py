# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:00:09 2021

@author: u0101727
"""

import os
import numpy as np

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
camera = '7'

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
pathVideosCam = os.path.join(pathVideosSubject, 'Cam{}'.format(camera))
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
