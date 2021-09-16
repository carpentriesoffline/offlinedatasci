#imports
import urllib.request, urllib.error, urllib.parse
import re
from datetime import datetime
import os
import glob


def file_search(filenamepattern): 
  for filename in glob.glob(filenamepattern):
    if os.path.isfile(filename):
      parsed=re.split("[_.]", filename)
      print(parsed)



#re.search(r'(\d{4})[/.-](\d{2})[/.-](\d{2})', date_line) 
#re.findall(r"[\w']+", DATA)
x=file_search("r_*_html_*.txt")