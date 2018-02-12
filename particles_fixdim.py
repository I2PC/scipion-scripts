#!/usr/bin/env python
"""
This script load a protocol from a given project to 
export the outputParticles as an stack of images.
"""
import sys, os

from pyworkflow.manager import Manager
import pyworkflow.utils as pwutils
import pyworkflow.em as em

from pyworkflow.em.packages.relion import ProtRelionRefine3D


def usage(error):
    print """
    ERROR: %s

    Usage: scipion python export_particles.py PROJECT PROCOTOL
        PROJECT: provide the project name
        PROCOTOL: provide the protocol id to be used as input.
    """ % error
    sys.exit(1)

argc = len(sys.argv)

if argc < 3 or argc > 4:
    usage("Incorrect number of input parameters")

projName = sys.argv[1]
protId = sys.argv[2]

manager = Manager()

if not manager.hasProject(projName):
    usage("Unexistent project: %s" % pwutils.red(projName))
    
project = manager.loadProject(projName)

prot = project.getProtocol(protId)

if prot is None:
    usage("Unexistent protocol: %s" % protId)

outputParticles = getattr(prot, 'outputParticles', None)

if outputParticles is None:
    usage("Protocol does not have 'outputParticles'")

realDims = outputParticles.getDimensions()
print "Real dimensions: ", realDims
print "DB dimensions: ", outputParticles.getDim()

# Set the new dimensions
outputParticles.setDim(realDims)
outputParticles.write()
project.mapper.store(prot)
project.mapper.commit()




