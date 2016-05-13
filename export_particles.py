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

    Usage: scipion python export_particles.py PROJECT PROCOTOL output_stack
        PROJECT: provide the project name to execute the workflow.
        PROCOTOL: provide the protocol id to be used as input.
        output_stack: stack file to write particles.
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

outputStack = sys.argv[3]

outputParticles.printAll()


print "Writing particles to : %s" % outputStack
t = pwutils.Timer()
t.tic()

outputParticles.writeStack(outputStack)
   
t.toc()

