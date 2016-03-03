#!/usr/bin/env python

"""
This scripts read a .sqlite file that contains a SetOfMovies
and write the filename names to a plain text file.

This script can be easily extended to write more Movies properties
or even to export other type of sets such as particles, ctf, etc.
"""

import sys
from pyworkflow.em.data import SetOfMovies



moviesSqlite = sys.argv[1]
outputFile = sys.argv[2]

movieSet = SetOfMovies(filename=moviesSqlite)

f = open(outputFile, 'w')

for movie in movieSet:
    f.write('%s\n' % movie.getFileName())
    
f.close()
