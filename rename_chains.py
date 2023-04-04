#!/usr/bin/env python
"""
This script load a atom struct from a given protocol/project 
splits it in all its chains, delete some of the chains,
rename others and finally reasembly the atom struct
"""
import sys, os

import pyworkflow as pw
from pyworkflow.project import Manager
from pyworkflow.project import Project
import pyworkflow.utils as pwutils

PROJECTNAME = 'projctname' # project name
PROCOTOLID = 1 # protocol used as input


projName = 'bi22006-model_building'
protId = 2

manager = Manager()

if not manager.hasProject(projName):
    print("Unexistent project: %s" % pwutils.red(projName))
    
try:
    projectPath = os.readlink(manager.getProjectPath(projName))
except:
    projectPath = manager.getProjectPath(projName)

project = Project(pw.Config.getDomain(), projectPath)
project.load()   

# get input protocol
prot = project.getProtocol(protId)

if prot is None:
    print(f"Unexisting protocol: {protId}")

print("output", prot.outputPdb)
outputParticles = getattr(prot, 'outputPdb', None)

# if outputParticles is None:
#     usage("Protocol does not have 'outputParticles'")

# outputStack = sys.argv[3]

# outputParticles.printAll()


# print ("Writing particles to : %s" % outputStack)
# t = pwutils.Timer()
# t.tic()

# outputParticles.writeStack(outputStack)
   
# t.toc()

