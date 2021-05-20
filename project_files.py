#!/usr/bin/env python

""" 
This script check missing project links and remove them.

"""

import sys, os

input_dir = sys.argv[1]

#using code ripped from:
#http://www.5dollarwhitebox.org/drupal/node/84
#to convert to human readable format
def convert_bytes(bytes):
   bytes = float(bytes)
   if bytes >= 1099511627776:
      terabytes = bytes / 1099511627776
      size = '%.2fT' % terabytes
   elif bytes >= 1073741824:
      gigabytes = bytes / 1073741824
      size = '%.2fG' % gigabytes
   elif bytes >= 1048576:
      megabytes = bytes / 1048576
      size = '%.2fM' % megabytes
   elif bytes >= 1024:
      kilobytes = bytes / 1024
      size = '%.2fK' % kilobytes
   else:
      size = '%.2fb' % bytes
   return size

typesizeH = {}
typesize = {}
typecount = {}


try:
   for root, dirs, filenames in os.walk(input_dir):
      for fn in filenames:
         
         prefix, extension = os.path.splitext(fn)
         ext = extension.lower()
         
         if ext not in typesize:
            typecount[ext] = typesize[ext] = 0
            
         
         file = os.path.join(root, fn)
         if os.path.isfile(file):
            typesize[ext] += os.stat(file).st_size
            typecount[ext] += 1
            
except KeyboardInterrupt:
   pass

types = typesize.keys()
types.sort(cmp=lambda a,b: cmp(typesize[a], typesize[b]), reverse=True)

headers = ["Filetype", "Size", "Count"]
row_format = u"{:<10}{:<15}{:<20}"
print(row_format.format(*headers))

for ext in types:
   print(row_format.format(ext, convert_bytes(typesize[ext]), typecount[ext]))

