
# This script loads the the ctf values from the micrographs star file
# and set the proper values into the particles star file
# it assumes that the rlnMicrographName value match between the two 
# files
#
# This scripts requires Scipion to be installed in order to run
#
# Usage:
#  scipion run set_particles_ctf.py micrographs_ctf.star particles.star
# Output:
# 	particles_ctf.star

import sys, os

import pyworkflow.em.metadata as md
import pyworkflow.utils as pwutils

# Input files
micStar = sys.argv[1]
partStar = sys.argv[2]
# Outputs 
outputStar = pwutils.removeExt(partStar) + '_ctf.star'
outputMd = md.MetaData()

micDict = {}

for micRow in md.iterRows(micStar):
	micName = micRow.getValue('rlnMicrographName')
	micDict[micName] = (micRow.getValue('rlnDefocusU'),
					    micRow.getValue('rlnDefocusV'),
						micRow.getValue('rlnDefocusAngle'))
									
									
for partRow in md.iterRows(partStar):
	micName = partRow.getValue('rlnMicrographName')
	if micName in micDict:
		defU, defV, defA = micDict[micName]
		partRow.setValue('rlnDefocusU', defU)
		partRow.setValue('rlnDefocusV', defV)
		partRow.setValue('rlnDefocusAngle', defA)
		partRow.addToMd(outputMd)
	else:
		print "Warning: Missing micrograph: ", micName
	
outputMd.write(outputStar)
