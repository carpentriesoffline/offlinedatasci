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

from rich.console import Console
from rich.progress import (
    Progress, BarColumn, TextColumn,
    DownloadColumn, TransferSpeedColumn, TimeRemainingColumn,
    MofNCompleteColumn
)

console = Console()


def _reporthook(progress, task_id):
    """Create a urlretrieve reporthook that updates a Rich progress task."""
    def hook(count, block_size, total_size):
        if total_size > 0:
            progress.update(task_id, total=total_size,
                           completed=min(count * block_size, total_size))
        else:
            progress.update(task_id, advance=block_size)
    return hook


def _file_progress():
    return Progress(
        TextColumn("  {task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console
    )


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
        console.print(f"[red]Error downloading R: {e}[/red]")

    try:
        download_rstudio(ods_dir)
    except Exception as e:
        console.print(f"[red]Error downloading RStudio: {e}[/red]")

    try:
        download_r_packages(ods_dir)
    except Exception as e:
        console.print(f"[red]Error downloading R packages: {e}[/red]")

    try:
        download_lessons(ods_dir)
    except Exception as e:
        console.print(f"[red]Error downloading lessons: {e}[/red]")

    try:
        download_python(ods_dir)
    except Exception as e:
        console.print(f"[red]Error downloading Python: {e}[/red]")

    try:
        download_python_packages(ods_dir)
    except Exception as e:
        console.print(f"[red]Error downloading Python packages: {e}[/red]")

def download_and_save_installer(latest_version_url, destination_path, progress):
    """Download and save installer in user given path.

    Keyword arguments:
    latest_version_url -- Link to download installer
    destination_path -- Path to save installer
    progress -- Rich Progress instance to add a task to
    """
    destination_path = Path(destination_path)
    filename = destination_path.name
    if not destination_path.exists():
        task = progress.add_task(filename, total=None)
        urllib.request.urlretrieve(latest_version_url, destination_path,
                                  reporthook=_reporthook(progress, task))
    else:
        task = progress.add_task(f"[dim]{filename} (already downloaded)[/dim]", total=1)
        progress.update(task, completed=1)


def download_r(ods_dir):
    """Download most recent version of R installer (mac and windows) from CRAN

    Keyword arguments:
    destination_path -- Path to save installers
    """
    console.rule("[bold]Downloading R")
    destination_path = Path(Path(ods_dir), Path("R"))
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)

    latest_version_url = "https://cloud.r-project.org/bin/macosx/"
    r_current_version = find_r_current_version(latest_version_url)

    with _file_progress() as progress:
        download_r_windows(r_current_version, ods_dir, progress)
        download_r_macosx(r_current_version, ods_dir, progress)


def download_lessons(ods_dir):
    """Downloads the workshop lessons as rendered HTML.
    Keyword arguments:
    destination_path -- Path to save rendered HTML lessons
    """
    console.rule("[bold]Downloading Lessons")

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

    lesson_path = Path(Path(ods_dir), Path("lessons"))
    if not os.path.isdir(lesson_path):
        os.makedirs(lesson_path)

    dc_wget = ["wget", "-r", "-k", "-N", "-c", "--no-parent", "--no-host-directories"]
    sc_wget = ["wget", "-p", "-r", "-k", "-N", "-c", "-E", "-H", "-D",
               "swcarpentry.github.io", "-K", "--no-parent", "--no-host-directories"]

    lessons_to_run = (
        [(url, Path(lesson_path, "data-carpentry"), dc_wget) for url in dc_lessons]
        + [(url, Path(lesson_path, "library-carpentry"), dc_wget) for url in lc_lessons]
        + [(url, Path(lesson_path, "software-carpentry"), sc_wget) for url in sc_lessons]
    )

    with Progress(
        TextColumn("  {task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Downloading lessons", total=len(lessons_to_run))
        for url, dest, wget_args in lessons_to_run:
            subprocess.run(wget_args + ["-P", dest, url],
                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            progress.advance(task)

    add_lesson_index_page(lesson_path)

def download_rstudio(ods_dir):
    """Download RStudio installers"""
    console.rule("[bold]Downloading RStudio")
    destination_path = Path(Path(ods_dir), Path("rstudio"))
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    raw_version = requests.get('https://download1.rstudio.org/current.ver').text.strip()
    # raw_version looks like "2026.04.0+526.pro2"; URL slug uses "-" instead of "+" with no ".pro*" suffix
    version = re.sub(r'\.pro\d+$', '', raw_version).replace('+', '-')
    baseurl = 'https://download1.rstudio.org/electron'
    urls = [
        f"{baseurl}/windows/RStudio-{version}.exe",
        f"{baseurl}/macos/RStudio-{version}.dmg",
    ]
    with _file_progress() as progress:
        for url in urls:
            download_and_save_installer(url, Path(destination_path, os.path.basename(url)), progress)

def download_python(ods_dir):
    """Download Python installers

    Keyword arguments:
    ods_dir -- Directory to save installers
    """
    console.rule("[bold]Downloading Python")
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

    with _file_progress() as progress:
        for url in download_urls:
            download_and_save_installer(url, Path(destination_path, os.path.basename(url)), progress)

def find_r_current_version(url):
    """Determine the most recent version of R from CRAN

    Keyword arguments:
    url -- CRAN r-project URL
    """
    version_regex = r"(R\-\d+\.\d+\.\d)+\-(?:x86_64|arm64|win)\.(?:exe|pkg)"
    urlfile = requests.get(url)
    for line in urlfile:
        decoded = line.decode("utf-8") 
        match = re.findall(version_regex, decoded)
        if (match):
            r_current_version = match[0].strip(".exe").strip(".pkg")
            return r_current_version
    return None

def download_r_windows(r_current_version, ods_dir, progress):
    """Download the most recent version of R installer for Windows from CRAN.

    Keyword arguments:
    r_current_version -- The most recent version of R
    ods_dir -- Directory to save R installers
    progress -- Rich Progress instance to add a task to
    """
    baseurl = "https://cloud.r-project.org/bin/windows/base/"
    download_path = baseurl + r_current_version + "-win.exe"
    destination_path = Path(Path(ods_dir), Path("R"), Path(r_current_version + "-win.exe"))
    download_and_save_installer(download_path, destination_path, progress)

def download_r_macosx(r_current_version, ods_dir, progress):
    """Download the most recent version of R installer for MacOSX from CRAN.

    Keyword arguments:
    r_current_version -- The most recent version of R
    ods_dir -- Directory to save R installers
    progress -- Rich Progress instance to add a task to
    """
    baseurl = "https://cloud.r-project.org/bin/macosx/"
    download_path_arm64 = baseurl + "sonoma-arm64/base/" + r_current_version + "-arm64.pkg"
    destination_path_arm64 = Path(Path(ods_dir), Path("R"), Path(r_current_version + "-arm64.pkg"))
    download_and_save_installer(download_path_arm64, destination_path_arm64, progress)

    download_path_x86_64 = baseurl + "big-sur-x86_64/base/" + r_current_version + "-x86_64.pkg"
    destination_path_x86_64 = Path(Path(ods_dir), Path("R"), Path(r_current_version + "-x86_64.pkg"))
    download_and_save_installer(download_path_x86_64, destination_path_x86_64, progress)

def get_ods_dir(directory=Path.home()):
    """Get path to save downloads, create if it does not exist.

    Keyword arguments:
    directory -- Path to save downloads (defaults to user home path)
    """
    folder_path = Path(directory)
    if not folder_path.is_dir():
        console.print(f"\nCreating ods folder in {directory}")
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
    console.rule("[bold]Downloading R Packages")

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
    console.print("  Building CRAN mirror with miniCRAN (this may take a while)...")
    subprocess.run(["Rscript", minicranpath, ods_dir, custom_library_string, r_major_minor_version])


def download_python_packages(ods_dir,py_library_reqs = [ "matplotlib", "notebook","numpy", "pandas"] ):
    """Creating partial PyPI mirror of workshop libraries.

    Keyword arguments:
    ods_dir -- Directory to save partial Pypi mirror
    """
    console.rule("[bold]Downloading Python Packages")

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
        console.print("  Downloading packages for Linux (manylinux_2_17_x86_64)...")
        pypi_mirror.download(platform = ['manylinux_2_17_x86_64'], **parameters)
        console.print("  Downloading packages for macOS (macosx_10_12_x86_64)...")
        pypi_mirror.download(platform = ['macosx_10_12_x86_64'], **parameters)
    console.print("  Downloading packages for Windows (win_amd64)...")
    pypi_mirror.download(platform = ['win_amd64'], **parameters)
    console.print("  Creating PyPI mirror index...")
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
        console.print(f"[red]Error in function: {function.__name__}. Error: {str(e)}[/red]")
