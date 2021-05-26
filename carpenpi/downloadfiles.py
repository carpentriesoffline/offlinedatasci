import os
import wget
from pathlib import Path
import re
from urls import *

# absolute_path = os.path.abspath(__file__)
# print("Full path: " + absolute_path)
# print("Directory Path: " + os.path.dirname(absolute_path))

#Downloads of files
#Documents for updates
#wget.download(url = url5, out= 'windowsRlatest.txt')
#wget.download(url = url6, out='maclRlatest.txt')

def file_name(fileurl):
  filename = fileurl.split("/")[-1]
  print(filename)

def identify_file_os(filename):
  if re.search('.exe',filename):
    return("windows")
  elif re.search('.dmg',filename) or re.search('.pkg',filename):
    return("macos")
  else:
    print("Error")

def download_files(fileurl):
  filename = fileurl.split("/")[-1]
  os = identify_file_os(filename)

  directory = "./IBB/Downloads/" + os + "/"
  folder_path = Path(directory)
  file_directory = directory + filename
  file_path = Path (file_directory)

  if not folder_path.exists():
    print("\nCreating folder in " + directory)
    Path.mkdir(folder_path)
    print("Downloading file " + fileurl + " to " + directory)
    wget.download(url = fileurl, out = directory)
  elif not file_path.exists():
    print("\nFolder " + directory + " exists proceeding to download...")
    print("Downloading file " + fileurl + " to " + directory)
    wget.download(url = fileurl, out = file_directory)
  else:
    print("\n" + filename + " found in " + directory)
  print('-------------------------------------')

for i in range (len(urls)):
  download_files(urls[i]) 