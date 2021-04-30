"""
This script calls SCAPE.exe, reconstruct a video from frame-per-frame images,
and reconstruct the intrinsic and extrinsic matrices. 

@author: Antoine Falisse
"""

import os
import numpy as np
import pickle
from utils import storage2numpy

# %% User inputs
'''
Select camera index (0-23):
    '0': front
    '1': (1*15) 15deg clockwise
    '2': (2*15) 30deg clockwise
    '3': (3*15) 45deg clockwise
    '4': (4*15) 60deg clockwise (back)
    '5': (5*15) 75deg clockwise
    '6': (6*15) 90deg clockwise
    '7': (7*15) 105deg clockwise
    ...
'''
# cameras = ['0','2','4','20','22']
cameras = ['0']

'''
Select distance (m)
'''
distance = '3.5'

'''
Select fovy (deg)
'''
fov = 85.0

'''
Set to True if you want to fix the ground_pelvis coordinates. This might help
keeping the model within the window.
'''
fixPelvis = True

# %% Paths

pathBase = os.getcwd()
pathData = os.path.join(pathBase, 'data')
pathOsim = os.path.join(pathData, 'OSIM')

computername = os.environ.get('COMPUTERNAME', None)
if computername == "GBW-L-W2003": # Antoine's laptop
    pathBuild = 'C:/Users/u0101727/Documents/Visual Studio 2017/Projects/BASH/build'
elif computername == "DESKTOP-2SV6M42": # Antoine's desktop
    pathBuild = 'C:/Users/antoi/Documents/VS2017/BASH/build'
pathExe = os.path.join(pathBuild, 'Release', 'SCAPE.exe')

osimModelName = 'referenceScaledModel.osim'
pathOsimModel = os.path.join(pathOsim, osimModelName)

motFileName = 'referenceMotion.mot'
pathMotFile = os.path.join(pathOsim, motFileName)

motion = storage2numpy(pathMotFile)
time = motion['time']
if fixPelvis:    
    headers = motion.dtype.names
    # set pelvis coordinates to 0
    pelvis_headers = ['pelvis_tilt', 'pelvis_list', 'pelvis_rotation',
                      'pelvis_tx', 'pelvis_ty', 'pelvis_tz',
                      'pelvis_obliquity']
    
    motion_fixedPelvis = np.zeros((time.shape[0], len(headers)))
    for count, header in enumerate(headers):
        if not header in pelvis_headers:
            motion_fixedPelvis[:, count] = motion[header]
    from utils import numpy2storage
    pathMotFile = os.path.join(pathOsim, motFileName[:-4] + "_fixedPelvis.mot")
    numpy2storage(headers, motion_fixedPelvis, pathMotFile)
                
pathVideos = os.path.join(pathData, 'Videos')
pathVideosDataset = os.path.join(pathVideos, 'DatasetTest')
pathVideosSubject = os.path.join(pathVideosDataset, 'SubjectTest')
pathVideosTrial = os.path.join(pathVideosSubject, 'TrialTest')

baseModelDir = os.path.join(pathData, 'baselineModel/')

# loop over cameras
for camera in cameras:
    pathVideosCam = os.path.join(pathVideosSubject, 'Cam{}'.format(camera), "InputMedia", motFileName[:-4])
    if not os.path.exists(pathVideosCam):
        os.makedirs(pathVideosCam)
    
    # %% Generate images
    command = '"{}" --osim {} --mot {} --model {} --output {} --camera {} --distance {} --fov {}'.format(
        pathExe, pathOsimModel, pathMotFile, baseModelDir, pathVideosCam, camera, distance, fov)
    os.system(command)
    
    # %% Create video from images
    # Extract framerate from mot file - we should have one image per frame.    
    framerate_in = int(np.round(1/np.mean(np.diff(time))))
    # Fix output framerate to 60 Hz.
    # TODO not sure since we later want to use together with model based markers, so we should maybe keep the same frame rate
    framerate_out = 60
    
    # We start from image #2, since the first 2 are before presentation mode.
    # TODO check that out, risk of mismatch between this and model-base data
    commande_ffmpeg = "ffmpeg -framerate {} -start_number 2 -i {}/image%d.png -c:v libx264 -r {} -pix_fmt yuv420p {}/{}.mp4".format(
        framerate_in, pathVideosCam, framerate_out, pathVideosCam, motFileName[:-4])
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
    # We need to transform from openGL (G) to openCV (C)
    # R_CG = [1 0 0; 0 -1 0; 0 0 -1]    
    R_CG = np.array([
        [1., 0., 0.],
        [0., -1., 0.],
        [0., 0., -1.]
        ], dtype=np.float64)   
    
    extrinsicsFile = open("{}/parameters4Extrinsics.txt".format(pathVideosCam), "r")
    extrinsics_str = extrinsicsFile.readlines()    
    # Rotation
    R = np.zeros((3,3))
    for i in range(3):
        row = extrinsics_str[i].split(" ")    
        for j, elm in enumerate(row):
            if j < 3:
                R[i,j] = float(elm)
    cameraParams['rotation'] = np.dot(R_CG, R)
    # print(cameraParams['rotation'])
    
    # Translation
    t = np.zeros((3,1))
    row = extrinsics_str[3].split(" ")  
    for j, elm in enumerate(row):
            if j < 3:
                t[j,0] = float(elm)
    cameraParams['translation'] = np.dot(R_CG, t)
    # print(cameraParams['translation'])
    
    open_file = open("{}/cameraIntrinsicsExtrinsics.pickle".format(pathVideosCam), "wb")
    pickle.dump(cameraParams, open_file)
    open_file.close()
