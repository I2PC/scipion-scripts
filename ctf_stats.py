#!/usr/bin/env python
# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *
# * [1] SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'delarosatrevin@scilifelab.se'
# *
# **************************************************************************

""" 
This script will compute the statistics of the SetOfCTFs in a given project.
"""

import sys, os

from pyworkflow.manager import Manager
import pyworkflow.utils as pwutils
from pyworkflow.em.data import SetOfCTF


def usage(error):
    print """
    ERROR: %s
    
    Usage: scipion python ctf_stats.py PROJECT
        PROJECT: provide the project name in which the workflow will be executed.
    """ % error
    sys.exit(1)    


def getCtfStats(ctfSet):
    """ Compute some stats from a given set of ctf. """
    ctf = ctfSet.getFirstItem()
    minDefocus = ctf.getDefocusU()
    maxDefocus = ctf.getDefocusU()

    for ctf in ctfSet:
        minDefocus = min(minDefocus, ctf.getDefocusU(), ctf.getDefocusV())
        maxDefocus = max(maxDefocus, ctf.getDefocusU(), ctf.getDefocusV())

    return minDefocus, maxDefocus


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage("Incorrect number of input parameters")

    projName = sys.argv[1]

    # Create a new project
    manager = Manager()

    if not manager.hasProject(projName):
        usage("Unexistent project: %s" % pwutils.red(projName))

    project = manager.loadProject(projName)

    for run in project.getRuns():
        for outputName, output in run.iterOutputAttributes(SetOfCTF):
            print run.getRunName(), '-', outputName
            minDefocus, maxDefocus = getCtfStats(output)
            print "  defocus: (%0.4f - %0.4f)" % (minDefocus, maxDefocus)


