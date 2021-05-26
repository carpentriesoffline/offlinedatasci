from urls import *
import re
#For updating files
def version_search(dowloadfile,fileurl):
  fileversion=file_name(fileurl)
  with open(dowloadfile, 'r') as f:
    x = f.readlines()
    filenlines = len(x)

  for i in range(filenlines -1,-1,-1):
    if( re.findall('Last modified', x[i]) or re.findall('Last changed', x[i]) ):
      y = x[i]
      print( y + " found in line " + str(i))

