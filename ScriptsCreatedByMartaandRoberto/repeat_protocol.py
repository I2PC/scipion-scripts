#!/usr/bin/env python
"""
This script repeats a protol many times
varying some of the run parameters. 

"""
from pyworkflow.project import Manager
from pyworkflow.object import String


# user must modify thw following lines
listAlternative = [
    {"vector": "-123.945, 196.15, 375.96"},  # 1st copy
    {"vector": "-210.73, -43.145, 432.945"},
    {"vector": "-208.065, -5.485, 440.885"},
    {"vector": "-181.645, -63.74, 428.355"},
    {"vector": "-177.63, -27.64, 438.575"},
    {"vector": "-175.055, 10.9, 439.875"},
    {"vector": "-147.945, -49.39, 435.72"},
    {"vector": "-144.315, -12.655, 440.85"},
    {"vector": "-140.94, 24.665, 439.525"},
    {"vector": "-137.545, 61.215, 433.09"},
    {"vector": "-134.34, 96.81, 421.97"},
    {"vector": "-131.11, 130.48, 407.965"},
    {"vector": "-127.54, 163.775, 392.365"},
    {"vector": "-123.945, 196.15, 375.96"},
    {"vector": "-114.35, -34.29, 438.94"},
    {"vector": "-111.09, 2.91, 440.985"},
    {"vector": "-107.695, 39.94, 437.91"},
    {"vector": "-104.44, 76.405, 430.6"},
    {"vector": "-101.02, 111.9, 419.6"},
    {"vector": "-97.535, 146.07, 406.185"},
    {"vector": "-94.195, 179.52, 391.355"},
    {"vector": "-81.325, -19.005, 440.595"},
    {"vector": "-77.835, 18.215, 440.465"},
    {"vector": "-74.46, 55.2, 436.005"},
    {"vector": "-71.115, 91.465, 427.94"},
    {"vector": "-67.7, 126.855, 416.95"},
    {"vector": "-64.14, 161.385, 403.775"},
    {"vector": "-47.865, -3.6, 441.3"},
    {"vector": "-44.535, 33.61, 439.37"},
    {"vector": "-41.125, 70.39, 433.785"},
    {"vector": "-37.7, 106.52, 425.02"},
    {"vector": "-34.23, 141.76, 413.625"},
    {"vector": "-14.825, 11.795, 441.23"},
    {"vector": "-11.29, 48.885, 437.945"},
    {"vector": "-7.835, 85.49, 431.08"},
    {"vector": "-4.16, 121.32, 421.185"},
    {"vector": "-0.405, 156.12, 409.285"},
]
projName = '2022_06_20_mx2369_pkv_CONT'
protId = 11772
parallelCopies = 5
# Do NOT edit anything beyond this point


# Create a new project manager
manager = Manager()    
project = manager.loadProject(projName)
inProtocol = project.getProtocol(protId)
protocolNameClass = type(inProtocol).__name__  #  protocol class name
# protocolPackage = type(inProtocol).__module__  # protocol module
# protClass =  Domain.importFromPlugin(protocolPackage, protocolName)  # import the module
# definitionDict = inProtocol.getDefinitionDict()  # definition Dict  # get all parameters avaialble in the form

counter = 1  # counter
objLabel = inProtocol.getObjLabel()
wait = False
for alternative in listAlternative:
    copyProtocol = project.copyProtocol(inProtocol)
    copyProtocol.setObjLabel(f'copy_#{counter} {objLabel}')
    for k, v in alternative.items():
        setattr(copyProtocol, k, String(v))
    print(f"executing protocol {protocolNameClass} with parameters {copyProtocol.getDefinitionDict()}" )
    project.launchProtocol(copyProtocol, wait=wait)
    if (counter % parallelCopies) == 0:
        wait = True
    else:
        wait = False
    counter += 1
