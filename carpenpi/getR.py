from datetime import datetime
import os
import re
import urllib.request, urllib.error, urllib.parse
import glob
import os.path

cwd = os.getcwd()

localreleasefilewin = cwd+"/windowsversion.txt"
localreleasefilemac = cwd+"/r_mac_html_2021-11-01.txt"
windowscranurlbase="https://cran.r-project.org/bin/windows/base/"
maccranurlbase = "https://cran.r-project.org/bin/macosx/base/"
fileregex = "(R\-\d+\.\d+\.\d+(?:\-[a-zA-Z]+)?\.(?:exe|pkg))"
latest_version_url_win= "https://cran.r-project.org/bin/windows/base/release.html"
latest_version_url_mac="https://cran.r-project.org/bin/macosx/"




def download_r_mostcurrentver(file,filepattern):
    urlfile = urllib.request.urlopen(file)
    for line in urlfile:
        decoded = line.decode("utf-8") 
  
        match = re.findall(filepattern, decoded)
        if (match):
            rcurrentversion = match
            if rcurrentversion[0].endswith('.exe'):
                baseurl="https://cran.r-project.org/bin/windows/base/"
            elif rcurrentversion[0].endswith('.pkg'):
                baseurl="https://cran.r-project.org/bin/macosx/base/"

            urllib.request.urlretrieve(baseurl+rcurrentversion[0], cwd + "/" + rcurrentversion[0])
            print("R file: " + rcurrentversion[0]+ " has been downloaded")


                                #forMAC
                                #if 'Latest release' in line:
                                #for line in g:
                                #match = re.findall(version_matcher, line)
            break  


download_r_mostcurrentver(latest_version_url_win,fileregex)

download_r_mostcurrentver(latest_version_url_mac,fileregex)



