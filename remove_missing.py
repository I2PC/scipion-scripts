
# This script loads the the ctf values from the micrographs star file
# and set the proper values into the particles star file
# it assumes that the rlnMicrographName value match between the two 
# files
#
# This scripts requires Scipion to be installed in order to run
#
# Usage:
#  scipion run remove_missing.py input_particles.star [output_particles.star]
# Output:
# 	Another star file only containing the items that image exists

import sys, os

import pyworkflow.em.metadata as md
import pyworkflow.utils as pwutils

# Input files
inputStar = sys.argv[1]

if len(sys.argv) > 2:
    outputStar = sys.argv[2]
else:
    outputStar = pwutils.removeExt(inputStar) + '_existing.star'

outputMd = md.MetaData()

fnDict = {}
index = None
IMG = 'rlnImageName'
MIC = 'rlnMicrographName'

for row in md.iterRows(inputStar):
    label = IMG if row.hasLabel(IMG) else MIC
    fn = row.getValue(label)

    if '@' in fn:
        index, fn = fn.split('@')

    if fn not in fnDict:
        fnDict[fn] = os.path.exists(fn)

    # Copy the item to the output md if the filename exists
    if fnDict[fn]:
        row.addToMd(outputMd)

print "Writing output to: %s" % outputStar
outputMd.write(outputStar)

pwutils.prettyDict(fnDict)
