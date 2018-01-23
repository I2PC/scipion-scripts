#!/usr/bin/env python

""" 
This script check missing project links and remove them.

"""

import sys, os

from pyworkflow.manager import Manager
import pyworkflow.utils as pwutils

ALL_RELATIONS = 'all'

def usage(error):
    print """
    ERROR: %s
    
    """ % error
    sys.exit(1)    

delete = '--delete' in sys.argv

# Create a new project
manager = Manager()
missing = []

for projName in os.listdir(manager.PROJECTS):
    entry = manager.getProjectPath(projName)
    #print " entry: ", entry, " islink: ", os.path.islink(entry), " exists: ", os.path.exists(entry)
    if os.path.islink(entry) and not os.path.exists(entry):
        missing.append(entry)

if missing:
    print "Missing projects:"
    print " \n".join(missing)

    if delete:
        for entry in missing:
            print "Removing: ", entry
            os.remove(entry)