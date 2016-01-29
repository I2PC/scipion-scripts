#!/usr/bin/env python

""" 
This script runs a workflow template automatically in an existing project.

TODO:
- Allow to create the project if not exists.
- Check the dependency graph between the runs.
"""

import sys, os

from pyworkflow.manager import Manager
import pyworkflow.utils as pwutils


def usage(error):
    print """
    ERROR: %s
    
    Usage: scipion run scripts/run_workflows.py PROJECT JSON_FILE [ARGS]
        PROJECT: provide the project name in which the workflow will be executed.
        JSON_FILE: the json file containing the workflow template to be executed.
        [ARGS]: specify some parameters to override the ones in the template.
            To change protocol label (protocol id=1) label:  1.object.label="import from A"
            To set param filePaths (protocol id=1):          1.filesPath="/path/to/files/"
    """ % error
    sys.exit(1)    


if len(sys.argv) != 3:
    usage("Incorrect number of input parameters")

projName = sys.argv[1]
jsonFile = os.path.abspath(sys.argv[2])
args = sys.argv[3:]

# Create a new project
manager = Manager()

if not manager.hasProject(projName):
    usage("Unexistent project: %s" % pwutils.red(projName))
    
if not os.path.exists(jsonFile):
    usage("Unexistent json file: %s" % pwutils.red(jsonFile))
    
project = manager.loadProject(projName)

protDict = project.loadProtocols(jsonFile)

# Now assuming that there is no dependencies between runs
# and the graph is lineal
for protId, prot in protDict.iteritems():
    project.launchProtocol(prot, wait=True)
    
