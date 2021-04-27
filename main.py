# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:00:09 2021

@author: u0101727
"""

import os

pathBase = os.getcwd()
pathData = os.path.join(pathBase, 'data')
pathOsim = os.path.join(pathData, 'OSIM')
pathExe = os.path.join(pathBase, 'build', 'x64', 'Release', 'SCAPE.exe')

osimModelName = 'subject3_c33_new.osim'
pathOsimModel = os.path.join(pathOsim, osimModelName)

motFileName = 'IK_c33_99.mot'
pathMotFileName = os.path.join(pathOsim, motFileName)

camera = '1'

pathVideos = os.path.join(pathData, 'Videos')
pathVideosDataset = os.path.join(pathVideos, 'DatasetTest')
pathVideosSubject = os.path.join(pathVideosDataset, 'SubjectTest')
pathVideosTrial = os.path.join(pathVideosSubject, 'TrialTest')
pathVideosCam = os.path.join(pathVideosSubject, 'Cam{}'.format(camera))
if not os.path.exists(pathVideosCam):
    os.makedirs(pathVideosCam)
    
baseModelDir = os.path.join(pathData, 'baselineModel/')

command = "{} --osim {} --mot {} --model {} --output {} --camera {}".format(
    pathExe, pathOsimModel, pathMotFileName, baseModelDir, pathVideosCam, camera)
os.system(command)
