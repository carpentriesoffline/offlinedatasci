#imports
import subprocess
import linecache
import re
from datetime import datetime
import os

#URLS of pages
urlwin = "https://cran.r-project.org/bin/windows/base"
urlmac = "https://cran.r-project.org/bin/macosx/"

path = "./"
subprocess.run(["wget", "-nc", "-P", path, urlwin])
subprocess.run(["wget", "-nc", "-P", path, urlmac])


string1 = ["LAST CHANGE", "LAST MODIFIED"]
file0 = "./base"
#"/home/pi/Desktop/web-free-data-science/carpenpi/software_htmls/base.txt"

for root, dirs, files in os.walk("./",topdown=False):
  print(files)

file1 = open(file0, "r")
for x in string1:
  index = 0
  flag = 0
  for root, dirs, files in os.walk("./",topdown=False):
    print(files)
    for line in files:
      index += 1
      if (x.upper() in  line.upper()):
        flag = 1
        break
      if flag == 0:
        print('String:', x, 'NOT Found')
      else:
        print('String:', x, 'FOUND In Line', index)
      messydate = linecache.getline(files,77)
      match = re.search(r'\d{4}-\d{2}-\d{2}', messydate)
      print(match)
      datex=datetime.strptime(match.group(), '%Y-%m-%d').date()
      print(datex)

      new_file = name + "_" + str(datex) + ".txt"
      print(new_file)

      os.rename(files, new_file)

  # closing text file
      files.close()
#Mac
#<p>Last modified: 2021/05/20, by Simon Urbanek</p>
#https://cran.r-project.org/bin/macosx/base/R-4.1.0.pkg

#windows
#<p>Last change: 2021-08-10</p>
#https://cran.r-project.org/bin/windows/base/R-4.1.1-win.exe

#Base

#https://cran.r-project.org/bin/

#windows
#R-4.1.1-win.exe

#mac base/R-4.1.0.pkg
