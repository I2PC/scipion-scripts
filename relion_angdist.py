
import sys
import pyworkflow.em.metadata as md
from pyworkflow.em.packages.relion import RelionPlotter

RelionPlotter.setBackend('TkAgg')


def error(msg):
    print "\nERROR: %s" % msg
    print("\nThis script show the angular distribution of Relion 3D refinement "
          " or classification as 2D plots in a Matplotlib figure. ")
    print "\nUSAGE: scipion python relion_angdist.py DATA_STAR_FILE [CLASSES]"
    print "   Where:"
    print "        DATA_STAR_FILE: input star files, e.g., run1_it011_data.star"
    print "        CLASSES[optional]: subset of classes, e.g., 1 2\n"
    sys.exit(1)


def createAngDistribution(inputMd, splitLabel, classes):
    # List of list of 3 elements containing angleTilt, anglePsi, weight
    projectionListDict = {}

    def getCloseProjection(angleRot, angleTilt, projectionList):
        """ Get an existing projection close to angleRot, angleTilt.
        Return None if not found close enough.
        """
        for projection in projectionList:
            if (abs(projection[0] - angleRot) <= 0.01 and
                abs(projection[1] - angleTilt) <= 0.01):
                return projection
        return None

    weight = 1.

    for row in md.iterRows(inputMd):
        splitValue = row.getValue(splitLabel)

        if classes and splitValue not in classes:
            continue

        angleRot = row.getValue('rlnAngleRot')
        angleTilt = row.getValue('rlnAngleTilt')

        if splitValue is None:
            raise Exception('Label %s not found' % md.label2Str(splitLabel))

        if not splitValue in projectionListDict:
            projectionListDict[splitValue] = []

        projectionList = projectionListDict[splitValue]
        projection = getCloseProjection(angleRot, angleTilt, projectionList)

        if projection is None:
            projectionList.append([angleRot, angleTilt, weight])
        else:
            projection[2] = projection[2] + weight

    return projectionListDict


def createPlot(inputStar, classes):

    inputMd = md.MetaData(inputStar)

    if inputMd.containsLabel(md.RLN_PARTICLE_RANDOM_SUBSET):
        splitLabel = md.RLN_PARTICLE_RANDOM_SUBSET
        prefix = 'half'
    else:
        splitLabel = md.RLN_PARTICLE_CLASS
        prefix = 'class'

    projectionListDict = createAngDistribution(inputMd, splitLabel, classes)

    nProj = len(projectionListDict)
    nRows = (nProj + 1) / 2
    nCols = 2 if nProj > 1 else 1

    plotter = RelionPlotter(x=nRows, y=nCols,
                            windowTitle="Angular Distribution")

    for key, projectionList in projectionListDict.iteritems():
        rot = []
        tilt = []
        weight = []
        n = len(projectionList)

        for r, t, w in projectionList:
            rot.append(r)
            tilt.append(t)
            weight.append(w/n) # normalize weights between 0 and 1

        plotter.plotAngularDistribution("%s_%03d" % (prefix, key),
                                       rot, tilt, weight)

    plotter.show(block=True)





if __name__ == '__main__':
    n = len(sys.argv)

    if n < 2:
        error("The input star file is required.")

    if n > 2:
        classes = [int(c) for c in sys.argv[2:]]
    else:
        classes = None

    inputStar = sys.argv[1]

    createPlot(inputStar, classes)