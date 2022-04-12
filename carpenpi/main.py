#Creating directory for R files if it does not exist
# Download files using download files.py
#Downloading Data Carpentry website using httrack

from pathlib import Path
from carpenpi import urls
from carpenpi import downloadfiles
from carpenpi import download_lessons

import bs4 as bs
from downloadfunction import *
import os
import re
import subprocess
import urllib.request, urllib.error, urllib.parse

def create_carpenpi_dir(directory=Path.home()):
    folder_path = Path(directory, Path('carpenpi'))
    if not folder_path.is_dir():
        print("\nCreating carpenpi folder in " + str(directory))
        Path.mkdir(folder_path, parents=True)
    return str(folder_path)

def download_and_save_installer(latest_version_url, destination_path):
    if not os.path.exists(destination_path):
                print("****File does not exists: ", destination_path)    
                urllib.request.urlretrieve(latest_version_url, destination_path) 
    else:
        print("Not being downloaded")


def download_and_save_r_installer(destination_path):
    latest_version_url_win = "https://cran.r-project.org/bin/windows/base/release.html"
    latest_version_url_mac = "https://cran.r-project.org/bin/macosx/"

    download_r_most_current_ver(latest_version_url_win, destination_path)
    download_r_most_current_ver(latest_version_url_mac, destination_path)


def download_lessons(carpenpi_dir):
    dc_lessons = ["https://datacarpentry.org/ecology-workshop/",
                  "https://datacarpentry.org/spreadsheet-ecology-lesson/",
                  "http://datacarpentry.org/OpenRefine-ecology-lesson/",
                  "https://datacarpentry.org/R-ecology-lesson/",
                  "https://datacarpentry.org/python-ecology-lesson/",
                  "https://datacarpentry.org/sql-ecology-lesson/"]
    
    sc_lessons = ["http://swcarpentry.github.io/shell-novice",
                  "http://swcarpentry.github.io/git-novice",
                  "http://swcarpentry.github.io/python-novice-inflammation",
                  "http://swcarpentry.github.io/python-novice-gapminder",
                  "http://swcarpentry.github.io/r-novice-inflammation",
                  "http://swcarpentry.github.io/r-novice-gapminder",
                  "http://swcarpentry.github.io/shell-novice-es",
                  "http://swcarpentry.github.io/git-novice-es",
                  "http://swcarpentry.github.io/r-novice-gapminder-es"]

    lessons = dc_lessons + sc_lessons
    for lesson in lessons:
        subprocess.run(["wget", "-r", "-k", "-N", "-c", "--no-parent", "-P", carpenpi_dir, lesson])

def download_Rstudio(carpenpi_dir):
    url = 'https://www.rstudio.com/products/rstudio/download/#download'
    r_studio_versions = {}
    fp = urllib.request.urlopen(url)
    web_content = fp.read()
    soup = bs.BeautifulSoup(web_content, 'lxml')
    r_studio_download_table = soup.find_all('table')[1]
    table_body = r_studio_download_table.find('tbody')
    r_studio_versions = {}
    for row in table_body.find_all("tr"):
      os_data = r_studio_parse_version_info(row)
      os_version = os_data["osver"] 
      r_studio_versions[os_version] = os_data
    for key in r_studio_versions.keys():
        if key.startswith("mac") or key.startswith("Win") :
          download_link = r_studio_versions[key]["url"]
          print(os.path.basename(download_link))
          download_and_save_installer(download_link, carpenpi_dir + "/" + os.path.basename(download_link))

def download_r_most_current_ver(file, path):
    # This regex will help find latest version for mac or windows
    # Format: R-4.1.2.pkg or R-4.1.2-win.exe
    version_regex = "(R\-\d+\.\d+\.\d+(?:\-[a-zA-Z]+)?\.(?:exe|pkg))"
    urlfile = urllib.request.urlopen(file)
    for line in urlfile:
        decoded = line.decode("utf-8") 
  
        match = re.findall(version_regex, decoded)
        if (match):
            r_current_version = match
            if r_current_version[0].endswith(".exe"):
                baseurl = "https://cran.r-project.org/bin/windows/base/"
            elif r_current_version[0].endswith('.pkg'):
                baseurl = "https://cran.r-project.org/bin/macosx/base/"
            download_path = baseurl + r_current_version[0]
            destination_path = path + "/" + r_current_version[0]
            print("\nDestination: ", destination_path, "\nDownload path: ", download_path)

            if not os.path.exists(destination_path):
                print("****file does not exists: ", destination_path)
                # urllib.request.urlretrieve(download_path, destination_path)
            break  

def r_studio_parse_version_info(row):
  # OS / LINK / SIZE / SHA-256
  columns = row.find_all("td") # find all columns in row
  os = columns[0].text.strip() # return first column data (OS)
  link = columns[1].a # return second column data (href) and access atag with href
  link_url = link['href'].strip()
  link_inner_html = link.text.strip()
  return {"osver": os, "version": link_inner_html, "url": link_url}        


