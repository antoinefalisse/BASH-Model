import numpy as np
import pandas as pd
import os

# %%  Found here: https://github.com/chrisdembia/perimysium/ => thanks Chris
def storage2numpy(storage_file, excess_header_entries=0):
    """Returns the data from a storage file in a numpy format. Skips all lines
    up to and including the line that says 'endheader'.
    Parameters
    ----------
    storage_file : str
        Path to an OpenSim Storage (.sto) file.
    Returns
    -------
    data : np.ndarray (or numpy structure array or something?)
        Contains all columns from the storage file, indexable by column name.
    excess_header_entries : int, optional
        If the header row has more names in it than there are data columns.
        We'll ignore this many header row entries from the end of the header
        row. This argument allows for a hacky fix to an issue that arises from
        Static Optimization '.sto' outputs.
    Examples
    --------
    Columns from the storage file can be obtained as follows:
        >>> data = storage2numpy('<filename>')
        >>> data['ground_force_vy']
    """
    # What's the line number of the line containing 'endheader'?
    f = open(storage_file, 'r')

    header_line = False
    for i, line in enumerate(f):
        if header_line:
            column_names = line.split()
            break
        if line.count('endheader') != 0:
            line_number_of_line_containing_endheader = i + 1
            header_line = True
    f.close()

    # With this information, go get the data.
    if excess_header_entries == 0:
        names = True
        skip_header = line_number_of_line_containing_endheader
    else:
        names = column_names[:-excess_header_entries]
        skip_header = line_number_of_line_containing_endheader + 1
    data = np.genfromtxt(storage_file, names=names,
            skip_header=skip_header)

    return data

def storage2df(storage_file, headers):
    # Extract data
    data = storage2numpy(storage_file)
    out = pd.DataFrame(data=data['time'], columns=['time'])    
    for count, header in enumerate(headers):
        out.insert(count + 1, header, data[header])    
    
    return out

def numpy2storage(labels, data, storage_file):
    
    assert data.shape[1] == len(labels), "# labels doesn't match columns"
    assert labels[0] == "time"
    
    f = open(storage_file, 'w')
    f.write('name %s\n' %storage_file)
    f.write('datacolumns %d\n' %data.shape[1])
    f.write('datarows %d\n' %data.shape[0])
    f.write('range %f %f\n' %(np.min(data[:, 0]), np.max(data[:, 0])))
    f.write('endheader \n')
    
    for i in range(len(labels)):
        f.write('%s\t' %labels[i])
    f.write('\n')
    
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            f.write('%20.8f\t' %data[i, j])
        f.write('\n')
        
    f.close()
    
def addMarkers(pathReferenceModel, pathScaledModel, pathScaledModelBASH):
    
    import opensim 
    
    referenceModel = opensim.Model(pathReferenceModel)   
    referenceModel.initSystem()
    markerSet = referenceModel.get_MarkerSet()
    
    myModel = opensim.Model(pathScaledModel)
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
    myModel.printToXML(pathScaledModelBASH)
    