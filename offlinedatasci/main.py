#Creating directory for R files if it does not exist
# Download files using download files.py
#Downloading Data Carpentry website using httrack

from pathlib import Path
import airium
import bs4 as bs
import os
import re
import subprocess
import urllib.request, urllib.error, urllib.parse
import importlib_resources
import pypi_mirror
import requests
import shutil
import sys
import warnings

def add_lesson_index_page(lesson_path):
    """Add a basic landing page for lessons
    
    Uses the top-level directory name to group lessons into sections by source
    Then displays an unordered list of lessons within each source

    """
    lesson_path = Path(lesson_path)
    a = airium.Airium()
    a('<!DOCTYPE html>')
    sources = next(os.walk(lesson_path))[1]
    with a.html():
        for source in sources:
            with a.head():
                a.meta(charset="utf-8")
                a.title(_t="Lessons")
            with a.body():
                a.h1(_t="Lesson Material")
                a.h2(_t=source.replace('-', ' ').title())
            lessons = next(os.walk(Path(lesson_path, Path(source))))[1]
            with a.ul():
                for lesson in lessons:
                    with a.li():
                        lesson_index = Path(Path(source), Path(lesson), Path("index.html"))
                        with a.a(href = lesson_index):
                            a(lesson.replace('-', ' ').title())

    with open(Path(Path(lesson_path), Path("index.html")), "w+") as index_file:
        index_file.writelines(str(a))

def download_all(ods_dir):
    """Download all installers, repositories, and lesson materials.

    Each function will run even if others fail.

    Keyword arguments:
    ods_dir -- Directory to save installers and lesson materials
    """
    try:
        download_r(ods_dir)
    except Exception as e:
        print(f"Error downloading R: {e}")

    try:
        download_rstudio(ods_dir)
    except Exception as e:
        print(f"Error downloading RStudio: {e}")

    try:
        download_r_packages(ods_dir)
    except Exception as e:
        print(f"Error downloading R packages: {e}")

    try:
        download_lessons(ods_dir)
    except Exception as e:
        print(f"Error downloading lessons: {e}")

    try:
        download_python(ods_dir)
    except Exception as e:
        print(f"Error downloading Python: {e}")

    try:
        download_python_packages(ods_dir)
    except Exception as e:
        print(f"Error downloading Python packages: {e}")

def download_and_save_installer(latest_version_url, destination_path):
    """Download and save installer in user given path.

    Keyword arguments:
    latest_version_url -- Link to download installer
    destination_path -- Path to save installer
    """
    if not os.path.exists(destination_path):
                print("****Downloading file: ", destination_path)    
                urllib.request.urlretrieve(latest_version_url, destination_path) 
    else:
        print("File not being downloaded")


def download_r(ods_dir):
    """Download most recent version of R installer (mac and windows) from CRAN

    Keyword arguments:
    destination_path -- Path to save installers
    """
    destination_path = Path(Path(ods_dir), Path("R"))
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)

    latest_version_url = "https://cloud.r-project.org/bin/macosx/"
    r_current_version = find_r_current_version(latest_version_url)
    download_r_windows(r_current_version, ods_dir)
    download_r_macosx(r_current_version, ods_dir)


def download_lessons(ods_dir):
    """Downloads the workshop lessons as rendered HTML.
    Keyword arguments:
    destination_path -- Path to save rendered HTML lessons
    """

    if not shutil.which('wget'):
        warnings.warn("""wget not detected so not downloading lessons.

        wget needs to be installed on your computer to clone lesson websites.

        macOS: you can install wget using Xcode command line tools
               or using `conda install wget -c conda-forge` if you are using conda.
        
        Windows: you can download a wget binary from: https://eternallybored.org/misc/wget/
        """)
        return

    dc_lessons = ["https://datacarpentry.org/ecology-workshop/",
                  "https://datacarpentry.org/spreadsheet-ecology-lesson/",
                  "http://datacarpentry.org/OpenRefine-ecology-lesson/",
                  "https://datacarpentry.org/R-ecology-lesson/",
                  "https://datacarpentry.org/python-ecology-lesson/",
                  "https://datacarpentry.org/sql-ecology-lesson/"]
    lc_lessons = ["https://librarycarpentry.org/lc-overview/",
                  "https://librarycarpentry.org/lc-data-intro/",
                  "https://librarycarpentry.org/lc-shell/",
                  "https://librarycarpentry.org/lc-open-refine/",
                  "https://librarycarpentry.org/lc-git/",
                  ]

    lesson_path = Path(Path(ods_dir), Path("lessons"))
    if not os.path.isdir(lesson_path):
        os.makedirs(lesson_path)

    for lesson in dc_lessons:
        print(f"Downloading lesson from {lesson}")
        subprocess.run(["wget", "-r", "-k", "-N", "-c", "--no-parent", "--no-host-directories",
                        "-P", Path(lesson_path, "data-carpentry"), lesson],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        
    for lesson in lc_lessons:
        print(f"Downloading lesson from {lesson}")
        subprocess.run(["wget", "-r", "-k", "-N", "-c", "--no-parent", "--no-host-directories",
                        "-P", Path(lesson_path, "library-carpentry"), lesson],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)

    sc_lessons = ["http://swcarpentry.github.io/shell-novice",
                  "http://swcarpentry.github.io/git-novice",
                  "http://swcarpentry.github.io/python-novice-inflammation",
                  "http://swcarpentry.github.io/python-novice-gapminder",
                  "http://swcarpentry.github.io/r-novice-inflammation",
                  "http://swcarpentry.github.io/r-novice-gapminder",
                  "http://swcarpentry.github.io/shell-novice-es",
                  "http://swcarpentry.github.io/git-novice-es",
                  "http://swcarpentry.github.io/r-novice-gapminder-es"]

    # Software Carpentry lessons have external CSS so requires a more expansive search & rewriting to get all necessary files
    for lesson in sc_lessons:
        print(f"Downloading lesson from {lesson}")
        subprocess.run(["wget", "-p", "-r", "-k", "-N", "-c", "-E", "-H", "-D",
                        "swcarpentry.github.io", "-K", "--no-parent", "--no-host-directories",
                        "-P", Path(lesson_path, "software-carpentry"), lesson],
                       stdout = subprocess.DEVNULL,
                       stderr = subprocess.STDOUT)
        
    add_lesson_index_page(lesson_path)

def download_rstudio(ods_dir):
    """Download RStudio installers"""
    baseurl = 'https://www.rstudio.com/products/rstudio/download/#download'
    destination_path = Path(Path(ods_dir), Path("rstudio"))
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    fp = requests.get(baseurl)
    web_content = fp.content
    soup = bs.BeautifulSoup(web_content, 'lxml')
    links = soup.find_all('a')
    for link in links:
        if link.has_attr('href') and (".exe" in link['href'] or ".dmg" in link['href']):
            url = str(link['href'])
            download_and_save_installer(url, Path(Path(destination_path), Path(os.path.basename(url))))

def download_python(ods_dir):
    """Download Python installers

    Keyword arguments:
    ods_dir -- Directory to save installers
    """
    version = get_python_version()
    download_urls = [f"https://www.python.org/ftp/python/{version}/python-{version}.exe",
                     f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe",
                     f"https://www.python.org/ftp/python/{version}/python-{version}-arm64.exe",
                     f"https://www.python.org/ftp/python/{version}/python-{version}-macos11.pkg"
    ]
    #TODO: dynamically check for macos version (at some point it won't be macos11)

    destination_path = Path(Path(ods_dir), Path("python"))
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    for url in download_urls:
        destination_path2 = Path(Path(destination_path), Path(os.path.basename(url)))
        download_and_save_installer(url, destination_path2)

def find_r_current_version(url):
    """Determine the most recent version of R from CRAN

    Keyword arguments:
    url -- CRAN r-project URL
    """
    version_regex = "(R\-\d+\.\d+\.\d)+\-(?:x86_64|arm64|win)\.(?:exe|pkg)"
    urlfile = requests.get(url)
    for line in urlfile:
        decoded = line.decode("utf-8") 
        match = re.findall(version_regex, decoded)
        if (match):
            r_current_version = match[0].strip(".exe").strip(".pkg")
            return r_current_version
    return None

def download_r_windows(r_current_version, ods_dir):
    """Download the most recent version of R installer for Windows from CRAN.

    Keyword arguments:
    r_current_version -- The most recent version of R
    ods_dir -- Directory to save R installers
    """
    baseurl = "https://cloud.r-project.org/bin/windows/base/"
    download_path = baseurl + r_current_version + "-win.exe"
    destination_path = Path(Path(ods_dir), Path("R"), Path(r_current_version + "-win.exe"))
    if not os.path.exists(destination_path):
        print("****Downloading file: ", destination_path)
        urllib.request.urlretrieve(download_path, destination_path)

def download_r_macosx(r_current_version, ods_dir):
    """Download the most recent version of R installer for MacOSX from CRAN.

    Keyword arguments:
    r_current_version -- The most recent version of R
    ods_dir -- Directory to save R installers
    """
    baseurl = "https://cloud.r-project.org/bin/macosx/"
    download_path_arm64 = baseurl + "big-sur-arm64/base/" + r_current_version + "-arm64.pkg"
    destination_path_arm64 = Path(Path(ods_dir), Path("R"), Path(r_current_version + "-arm64.pkg"))
    if not os.path.exists(destination_path_arm64):
        print("****Downloading file: ", destination_path_arm64)
        urllib.request.urlretrieve(download_path_arm64, destination_path_arm64)

    download_path_x86_64 = baseurl + "big-sur-x86_64/base/" + r_current_version + "-x86_64.pkg"
    destination_path_x86_64 = Path(Path(ods_dir), Path("R"), Path(r_current_version + "-x86_64.pkg"))
    if not os.path.exists(destination_path_x86_64):
        print("****Downloading file: ", destination_path_x86_64)
        urllib.request.urlretrieve(download_path_x86_64, destination_path_x86_64)

def get_ods_dir(directory=Path.home()):
    """Get path to save downloads, create if it does not exist.

    Keyword arguments:
    directory -- Path to save downloads (defaults to user home path)
    """
    folder_path = Path(directory)
    if not folder_path.is_dir():
        print("\nCreating ods folder in " + str(directory))
        Path.mkdir(folder_path, parents=True)
    return str(folder_path)

def get_python_version(minor_version = "3.12"):
    """Determine the Python version from the Python homepage."""
    url = "https://www.python.org/ftp/python/"
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    versions = [a.text for a in soup.find_all('a') if a.text.startswith(minor_version)]
    latest_version = sorted(versions, reverse=True)[0].strip('/')
    return latest_version

def table_parse_version_info(row,oscolnum,hrefcolnum):
    """Parse and return software information from table.

    Keyword arguments:
    row -- Row from HTML table
    oscolnum -- Number of column in which OS is found
    hrefcolnum -- Number of column in which HREFs are found
    """
    # OS / LINK / SIZE / SHA-256
    columns = row.find_all("td") # find all columns in row
    os = columns[oscolnum].text.strip() # return first column data (OS)
    link = columns[hrefcolnum].a # return second column data (href) and access atag with href
    link_url = link['href'].strip()
    link_inner_html = link.text.strip()
    return {"osver": os, "version": link_inner_html, "url": link_url}        

def download_r_packages(ods_dir,
                      py_library_reqs = ["tidyverse", "RSQLite"],
                      r_version = None):
    """Creating partial CRAN mirror of workshop libraries.

    Keyword arguments:
    ods_dir -- Directory to create CRAN mirror
    """
    if not shutil.which('Rscript'):
        warnings.warn("""Rscript not detected so not installing miniCRAN.

        R needs to be installed on your computer to clone lesson websites.

        Install R from: https://cloud.r-project.org/
        """)
        return
    
    if r_version is None:
        r_version = find_r_current_version("https://cloud.r-project.org/bin/windows/base/")
    
    r_major_minor_version_nums = r_version.replace('R-', '').split('.')
    r_major_minor_version = '.'.join(r_major_minor_version_nums[:2])

    minicranpath = importlib_resources.files("offlinedatasci") / "miniCran.R"
    custom_library_string = ' '.join(py_library_reqs)
    subprocess.run(["Rscript", minicranpath, ods_dir, custom_library_string, r_major_minor_version])


def download_python_packages(ods_dir,py_library_reqs = [ "matplotlib", "notebook","numpy", "pandas"] ):
    """Creating partial PyPI mirror of workshop libraries.

    Keyword arguments:
    ods_dir -- Directory to save partial Pypi mirror
    """
    python_version = get_python_version()
    download_dir = Path(Path(ods_dir), Path("pythonlibraries"))
    pypi_dir = Path(Path(ods_dir), Path("pypi"))
    parameters = {
        'pip': 'pip3',
        'dest': download_dir,
        'pkgs': py_library_reqs,
        'python_version': python_version,
        'allow_binary': True
    }
    if sys.platform == 'win32':
        # pip download does not currently work for other OSs on Windows
        # Therefore we don't download mac and Linux packages on Windows
        # See https://github.com/pypa/pip/issues/11664
        warnings.warn("""Only mirroring Python packages for Windows
                      
        pip cannot currently download macos and Linux packages on Windows.
        See https://github.com/pypa/pip/issues/11664
        """)
    else:
        pypi_mirror.download(platform = ['manylinux_2_17_x86_64'], **parameters)
        pypi_mirror.download(platform = ['macosx_10_12_x86_64'], **parameters)
    pypi_mirror.download(platform = ['win_amd64'], **parameters)
    mirror_creation_parameters = {
        'download_dir': download_dir,
        'mirror_dir': pypi_dir,
        'copy': True
    }
    pypi_mirror.create_mirror(**mirror_creation_parameters)

def get_default_packages(package_type):
    packages = { 
        "r-packages": {
            "data-carpentry": ["tidyverse", "RSQLite"],
            "data-science": ["dplyr", "ggplot2", "shiny", "lubridate", "knitr", "esquisse", "mlr3", "knitr", "DT"]
        },
        "python-packages": {
            "data-carpentry": ["pandas", "notebook", "numpy", "matplotlib", "plotnine"], 
            "software-carpentry": ["matplotlib", "notebook", "numpy", "pandas"] ,
            "data-science": ["scipy", "numpy", "pandas", "matplotlib", "keras", "scikit-learn", "beautifulsoup4", "seaborn","torch"]
        }
    }
    return packages[package_type]


def package_selection(language, custom_package_list):
    language_dictionary = get_default_packages(language)
    packages_to_download = []
    for item in custom_package_list:
        if item in [*language_dictionary]:
            packages_to_download.extend(language_dictionary[item])
        else:
            packages_to_download.append(item)
    packages_to_download = list(set(packages_to_download))
    return packages_to_download

def try_except_functions(input, function):
    try:
        function(input)
    except Exception as e:
        print( f"Error in function: {function.__name__}. Error: {str(e)}")
