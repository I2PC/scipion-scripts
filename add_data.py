#!/usr/bin/env python
"""
Since in cryosparc many time the protocol aborts after computing the results
This script loads a volue and a set of particles 
and add them to a protocol

run as:
   scipion3 python ./add_data.py
from any directory
"""
import sys

from pyworkflow.project import Manager
import pyworkflow as pw
import pwem.objects as emobj

import pyworkflow.utils as pwutils
from pyworkflow.protocol import STATUS_FINISHED
# P3-J15 22090
# P3-J24 22521
# first step) Manually import objects that you want to add as protocol output
#             we perform this step in order to convert from cryosparc format to scipion

importParticlesID = 23791  # import protocol ID (particles)
importVolumeID = 23846  # import volume id (3D map)
cryoSparcProtocolID = 22521  # ID of cryoaprc protocol. Data will be added to this protocol
projName = '2022_06_20_mx2369_pkv_CONT_2' # project name
OUTPUTPARTICLESNAME = 'outputParticles_1'
OUTPUTVOLUMENAME = 'outputVolume_1'

#############################################################################
# DO NOT CHANGED ANYTHING AFTER THIS LINE UNLESS YOU KNOW WHAT YOUR ARE DOING
#############################################################################

manager = Manager()

# test project exists
if not manager.hasProject(projName):
    print("Unexistent project: %s" % pwutils.red(projName))
    sys.exit(1)

project = manager.loadProject(projName)
importParticlesProt = project.getProtocol(importParticlesID)
importVolumeProt = project.getProtocol(importVolumeID)
cryoSparcProtocolProt = project.getProtocol(cryoSparcProtocolID)

# test  protocols exist
if importParticlesProt is None:
    print("Unexistent protocol: %s" % importParticlesProt)
    sys.exit(1)
if importVolumeProt is None:
    print("Unexistent protocol: %s" % importVolumeProt)
    sys.exit(1)
if cryoSparcProtocolProt is None:
    print("Unexistent protocol: %s" % cryoSparcProtocolProt)
    sys.exit(1)

# get Input set of particles and volume
inParticles = getattr(importParticlesProt, 'outputParticles', None)  # cryosparc
inVolume = getattr(importVolumeProt, 'outputVolume', None)  # cryosparc
# IMPORTANT: this not does work, we need to update the status in
# the projects.sqlite file not in the protocol copy
# do it using sbeaver
cryoSparcProtocolProt.setStatus = STATUS_FINISHED

# attach to existing protocol
cryoSparcProtocolProt._defineOutputs(OUTPUTPARTICLESNAME=inParticles)
cryoSparcProtocolProt._defineOutputs(OUTPUTVOLUMENAME=inVolume)
cryoSparcProtocolProt._store(inParticles)
cryoSparcProtocolProt._store(inVolume)
