#Creating directory for R files if it does not exist
# Download files using download files.py
#Downloading Data Carpentry website using httrack

from pathlib import Path
import bs4 as bs
import os
import re
import subprocess
import urllib.request, urllib.error, urllib.parse
import pkg_resources
import pypi_mirror

def create_ods_dir(directory=Path.home()):
    """Get path to save downloads or make it

    Keyword arguments:
    directory (default Path.home())
    """
    folder_path = Path(directory)
    if not folder_path.is_dir():
        print("\Saving ods downloads in " + str(directory))
        Path.mkdir(folder_path, parents=True)
    return str(folder_path)

def download_and_save_installer(latest_version_url, destination_path): 
    if not os.path.exists(destination_path):
                print("****Downloading file: ", destination_path)    
                urllib.request.urlretrieve(latest_version_url, destination_path) 
    else:
        print("File not being downloaded")


def download_and_save_r_installer(destination_path):
    latest_version_url_win = "https://cran.r-project.org/bin/windows/base/release.html"
    latest_version_url_mac = "https://cran.r-project.org/bin/macosx/"

    download_r_most_current_ver(latest_version_url_win, destination_path)
    download_r_most_current_ver(latest_version_url_mac, destination_path)


def download_lessons(ods_dir):
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
        subprocess.run(["wget", "-r", "-k", "-N", "-c", "--no-parent", "-P", ods_dir, lesson])

def download_software(ods_dir,software):
    """Get path to save downloads or make it

    Keyword arguments:
    directory (default Path.home())
    """
    if software=="Rstudio":
        url = 'https://www.rstudio.com/products/rstudio/download/#download'
        download_table_num=1
        oscolnum=0
        hrefcolnum=1
        key="osver"
    elif software=="Python":
        url = 'https://www.python.org/downloads/release/python-3104/'
        download_table_num=0
        oscolnum=1
        hrefcolnum=0
        key="version"
    destination_path = Path(Path(ods_dir), Path(software))
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    r_studio_versions = {}
    fp = urllib.request.urlopen(url)
    web_content = fp.read()
    soup = bs.BeautifulSoup(web_content, 'lxml')
    r_studio_download_table = soup.find_all('table')[download_table_num]
    table_body = r_studio_download_table.find('tbody')
    r_studio_versions = {}
    for row in table_body.find_all("tr"):
      os_data = table_parse_version_info(row,oscolnum,hrefcolnum)
      os_version = os_data[key] 
      r_studio_versions[os_version] = os_data
    for key in r_studio_versions.keys():
        is_windows = "embeddable" not in key and "help" not in key and key.startswith("Windows")
        is_macos = key.startswith("macOS")
        if (is_macos or is_windows):
          download_link = r_studio_versions[key]["url"]
          print(os.path.basename(download_link))
          destination_path2 = Path(Path(destination_path), Path(os.path.basename(download_link)))
          download_and_save_installer(download_link, destination_path2)

def download_r_most_current_ver(file, ods_dir):
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
            destination_path = Path(Path(ods_dir), Path("R"))
            if not os.path.isdir(destination_path):
                os.makedirs(destination_path)

            destination_path2 = Path(Path(ods_dir), Path("r"), Path(r_current_version[0]))
            print("\nDestination: ", destination_path2, "\nDownload path: ", download_path)

            if not os.path.exists(destination_path2):
                print("****Downloading file: ", destination_path2)
                urllib.request.urlretrieve(download_path, destination_path2)
            break

def table_parse_version_info(row,oscolnum,hrefcolnum):
  """Parse and return software information from table

    Keyword arguments:
    row -- Row that is being passed
    oscolnum -- Number of column in which OS is found
    hrefcolnum -- Number of column in which hrefs are found
    """
  # OS / LINK / SIZE / SHA-256
  columns = row.find_all("td") # find all columns in row
  os = columns[oscolnum].text.strip() # return first column data (OS)
  link = columns[hrefcolnum].a # return second column data (href) and access atag with href
  link_url = link['href'].strip()
  link_inner_html = link.text.strip()
  return {"osver": os, "version": link_inner_html, "url": link_url}        

def find_call_minicran(ods_dir):
    minicranpath=pkg_resources.resource_filename("offlinedatasci", "miniCran.R")
    subprocess.run(["Rscript", minicranpath, ods_dir])


def python_libraries(ods_dir):
    """Creating partial PyPI mirror of workshop libraires

    Keyword arguments:
    ods_dir -- Directory to save mirror
    """
    #workshop_needed_libraries = pandas, matplotlib, numpy
    #python_included_libraries = math, random, glob, time, sys, pathlib
    py_library_reqs = [ "matplotlib", "notebook","numpy", "pandas"]
    download_dir = Path(Path(ods_dir), Path("pythonlibraries"))
    pypi_dir = Path(Path(ods_dir), Path("pypi"))
    parameters = {
        'pip': 'pip3',
        'dest': download_dir,
        'pkgs': py_library_reqs,
        'python_version': '3.9.6'
    }
    pypi_mirror.download(platform = [ 'manylinux1_x86_64'], **parameters)
    pypi_mirror.download(platform = [ 'macosx_10_10_x86_64'], **parameters)
    pypi_mirror.download(platform = [ 'win_amd64'], **parameters)
    mirror_creation_parameters = {
    'download_dir': download_dir,
    'mirror_dir': pypi_dir
    }
    pypi_mirror.create_mirror(**mirror_creation_parameters)





