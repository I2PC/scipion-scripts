#!/usr/bin/env python
"""
This script repeats a two steps of the workflow many times
varying some of the run parameters. 

It can be modified to be used for other cases.
"""
import sys

from pyworkflow.manager import Manager
import pyworkflow.utils as pwutils
import pyworkflow.em as em
from pyworkflow.em.packages.relion import ProtRelionRefine3D


def usage(error):
    print """
    ERROR: %s

    Usage: scipion python run_steps.py PROJECT PROCOTOL [N=3]
        PROJECT: provide the project name to execute the workflow.
        PROCOTOL: provide the protocol id to be used as input.
        N: the number of times to repeat the workflow.
    """ % error
    sys.exit(1)

argc = len(sys.argv)

if argc < 3 or argc > 4:
    usage("Incorrect number of input parameters")

projName = sys.argv[1]
protId = sys.argv[2]

n = int(sys.argv[3]) if argc == 4 else 3 

# Create a new project
manager = Manager()

if not manager.hasProject(projName):
    usage("Unexistent project: %s" % pwutils.red(projName))
    
project = manager.loadProject(projName)

protExtractParts = project.getProtocol(protId)
protVol = project.getProtocol(1256)

protRelionAllParts = project.getProtocol(1291)
protRelionBestParts = project.getProtocol(1359)

project.launchProtocol(protRelionAllParts, wait=True)
project.launchProtocol(protRelionBestParts, wait=True)

for i in range(n):
    protSubSet = project.newProtocol(em.ProtSubSet,
                                     objLabel='Subset #%d' %n,
                                     chooseAtRandom=True,
                                     nElements=13245)
    
    protSubSet.inputFullSet.set(protExtractParts.outputParticles)
    project.launchProtocol(protSubSet, wait=True)
    
    relionRefine = project.copyProtocol(protRelionBestParts)
    relionRefine.objLabel.set('Refine Test #%d' %n)
    relionRefine.inputParticles.set(protSubSet.outputParticles)
    project.launchProtocol(relionRefine, wait=True)
