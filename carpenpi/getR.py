from datetime import datetime
import os
import re
from turtle import down
import urllib.request, urllib.error, urllib.parse

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


def download_and_save_r_installer(destination_path):
    latest_version_url_win = "https://cran.r-project.org/bin/windows/base/release.html"
    latest_version_url_mac = "https://cran.r-project.org/bin/macosx/"

    download_r_most_current_ver(latest_version_url_win, destination_path)
    download_r_most_current_ver(latest_version_url_mac, destination_path)

cwd = os.getcwd()
download_and_save_r_installer(cwd)