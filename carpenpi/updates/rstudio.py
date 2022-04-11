#imports
import bs4 as bs
from downloadfunction import *
#import downloadfunction as dof
import lxml
import os
import urllib.request, urllib.error, urllib.parse

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
