import os
import re
import urllib.request, urllib.error, urllib.parse


def download_and_save_installer(latest_version_url, destination_path):
    if not os.path.exists(destination_path):
                print("****File does not exists: ", destination_path)    
                urllib.request.urlretrieve(latest_version_url, destination_path) 
    else:
        print("Not being downloaded")

def r_studio_parse_version_info(row):
  # OS / LINK / SIZE / SHA-256
  columns = row.find_all("td") # find all columns in row
  os = columns[0].text.strip() # return first column data (OS)
  link = columns[1].a # return second column data (href) and access atag with href
  link_url = link['href'].strip()
  link_inner_html = link.text.strip()
  return {"osver": os, "version": link_inner_html, "url": link_url}        
