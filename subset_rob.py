#!/usr/bin/env python
"""
This script loads two sets of particles
(from two different protocols).
Then it compares the imges 
and saves the images that are identical in both sets.
The search will take adventage on the fact that
identical images has the same mic.name attribute
and almost the same coordinates x, y
Run with scipion 3.0.11
"""
import sys, os

from pyworkflow.project import Manager
from pyworkflow.project import Project
import pyworkflow as pw
import pwem.objects as emobj

import pyworkflow.utils as pwutils
import numpy as np
from pwem.emlib.image import ImageHandler
from scipy import signal
import timeit

# name of the project contaning the particleSets
projName = 'bi22006-4-delta7-july2019'
# ID of the protocols containing the particle sets
# protIdLarge contains almost protId
protId = 37549
protIdLarge = 79808

manager = Manager()

# test project exists
if not manager.hasProject(projName):
    print("Unexistent project: %s" % pwutils.red(projName))
    sys.exist(1)

##### READ set of particles, first set ##############
project = manager.loadProject(projName)
prot = project.getProtocol(protId)
protLarge = project.getProtocol(protIdLarge)
partSet = prot._createSetOfParticles(suffix='kk')
partSetLarge = protLarge._createSetOfParticles(suffix='pp')


# test  protocols exist
if prot is None:
    print("Unexistent protocol: %s" % protId)
if protLarge is None:
    print("Unexistent protocol: %s" % protIdLarge)

##### READ set of particles, second set ##############
inParticles = getattr(prot, 'outputParticles', None)
inParticlesLarge = getattr(protLarge, 'outputParticles', None)
partSetLarge.copyInfo(inParticles)
partSetLarge.setSamplingRate(inParticles.getSamplingRate())
partSetLarge.setAlignment(inParticles.getAlignment())

#  print number of particles in each set
print("inParticles", inParticles)
print("inParticlesLarge", inParticlesLarge)

if inParticles is None:
    print("Protocol does not have 'outputParticles'")

if inParticlesLarge is None:
    print("Protocol outputParticlesLarge does not have 'outputParticles'")


partSet.copyInfo(inParticles)
partSet.setAlignment(inParticles.getAlignment())
listOfMatrices = []
listOfMatricesLarge = [] 
# ih = ImageHandler()
# read small subset and save in memory micID, and x and y coordinates 

#ih = ImageHandler()
selected = -1
for particle in inParticles:
    id = particle.getObjId()
    data = particle.getCoordinate()
    micId = int(data._micId)
    coordinate_x = int(data._x)
    coordinate_y = int(data._y)
    #matrix = ih.read(particle.getLocation()).getData()
    listOfMatrices.append((id, micId, coordinate_x, coordinate_y))  # , matrix[95:145, 95:145]))

print("read small set")
start = timeit.timeit()
listOfMatrices = sorted(listOfMatrices, key=lambda x: (x[1], x[2], x[3]))
end = timeit.timeit()
print("sorted small set", end - start)

# read large subset
for particle in inParticlesLarge:
    id = particle.getObjId()
    data = particle.getCoordinate()
    micId = int(data._micId)
    coordinate_x = int(data._x)
    coordinate_y = int(data._y)
    #matrix = ih.read(particle.getLocation()).getData()
    listOfMatricesLarge.append((id, micId, coordinate_x, coordinate_y, selected))  #  matrix[95:145, 95:145]))
    # REMOVE NEXT LINE
    #if id >  199999:
    #    break

print("read large set")
start = timeit.timeit()
listOfMatricesLarge = sorted(listOfMatricesLarge, key=lambda x: (x[1], x[2], x[3]))
end = timeit.timeit()
print("sorted large set", end - start)

counterBase = 0
counterExtra = 0
counter = counterBase + counterExtra
resultListIdLarge = []
resultListId = []
doWhile = True

len_listOfMatrices = len(listOfMatrices)
size = len(listOfMatricesLarge)
### input("Press any key to continue")
doWhile = True

for i, matrixTuple in enumerate(listOfMatrices):
    if i%100 ==0:
        print(".")
    ### maxCorr = -1
    particle_parent = matrixTuple[1]  # get micID
    coord_x = matrixTuple[2]
    coord_y = matrixTuple[3]
    ## matrixSmall = matrixTuple[4]
    doWhile = True
    while doWhile:
       counter = counterBase + counterExtra
       #print("counter", counter)
       if counter >= size:
           counterExtra = 0
           ## print("No more elements in listOfMatricesLarge")
           ## doWhile = False
           break
       selected = listOfMatricesLarge[counter][-1]
       if selected > 0:
           counterExtra += 1
           continue
       # print("counter", counter)
       particle_parent_large = listOfMatricesLarge[counter][1]
       if particle_parent <  particle_parent_large:
           counterExtra = 0
           print("No match for particle", particle_parent)
           break  # next item from small list
       elif particle_parent >  particle_parent_large:
           counterBase += counterExtra + 1
           counterExtra = 0
       else:
            coord_xl = listOfMatricesLarge[counter][2]
            coord_yl = listOfMatricesLarge[counter][3]
            ##matrixLarge = listOfMatricesLarge[counter][4]
            #corrMatrix = signal.correlate2d(matrixSmall, matrixLarge)
            #corr = np.argmax(corrMatrix)
            #print("counter corr", counter, corr)
            ## if corr > maxCorr:  #  and corr > maxcorr  # may be corr > 05 if enough!!!!
            if abs(coord_x - coord_xl) <= 6 and abs(coord_y - coord_yl) <= 6:
                resultListIdLarge.append( (matrixTuple[0], listOfMatricesLarge[counter][0]))
                listOfMatricesLarge[counter] = listOfMatricesLarge[counter][:-1] + (1,) # particle selected do not use it again
                doWhile = False
                counterExtra = 0
                ## break ## may be break if corr > threshold
                ## otherwise it will break when counter >= size
            else:
                counterExtra += 1
                

print("RESULT")
resultListIdLarge = sorted(resultListIdLarge, key=lambda x: (x[1], x[0]))

# create output set
for idSmall, idLarge in resultListIdLarge:
    id = idLarge
    particle = inParticlesLarge.__getitem__(id)
    newParticle = particle.clone()
    partSetLarge.append(newParticle)
protLarge._defineOutputs(outputSet2=partSetLarge)
protLarge._store(prot)

print("Number of intersection particles", len(resultListIdLarge))
for match in resultListIdLarge:
    print(match)