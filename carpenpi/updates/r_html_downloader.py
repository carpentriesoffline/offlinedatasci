from datetime import datetime
import os
import re
import urllib.request, urllib.error, urllib.parse
import glob
import os.path

url_os = ["https://cran.r-project.org/bin/macosx/", "https://cran.r-project.org/bin/windows/base"]
url_filename = {
  "https://cran.r-project.org/bin/macosx/" : "r_mac_html", 
  "https://cran.r-project.org/bin/windows/base" : "r_win_html"
}
last_change_string = "last change"
last_modified_string = "last modified"


# Returns the line from downloaded html from url provided.
def parse_dateline_string(string):
      lowercase_line = string.lower()
      if last_change_string in lowercase_line or last_modified_string in lowercase_line:
        string_lower_match=lowercase_line
        #date_find(string_lower_match)

#Search for file name and returns date
def file_search(filenamepattern,path): 
  oldinfo=[]
  oldfileinfodic={"currentfilepath":[],"currentfiledate":[],"currentfileostype":[]};
  #keys = ["currentfilepath", "currentfiledate"]
  #oldfileinfodic= dict.fromkeys(keys)
  oldinfo=[]
  for filename in glob.glob(path + "r_*_html_*.txt"):
    if os.path.isfile(filename):
      olddate=filename.split("_")[-1].split(".")[0]
      oldinfo.extend([[filename, olddate, filename.split("_")[1]]])

      #Using dic of lists
      #oldfileinfodic["currentfilepath"].append(filename)
      #oldfileinfodic["currentfiledate"].append(olddate)
      #oldfileinfodic["currentfileostype"].append(filename.split("_")[1])
      #print (oldfileinfodic)
      #oldfileinfodic.update({'currentfilepath':filename, "currentfiledate": olddate });

       #dates_dict[key].append(date)
  #return (oldfileinfodic)
  return (oldinfo)


#Find,parse and return date in online file
def date_find(textline):
  date_match = re.search(r'(\d{4})[/.-](\d{2})[/.-](\d{2})', textline) # Search for string that matches yyyy/mm/dd or yyyy-mm-dd format.
  for fmt in ('%Y-%m-%d', '%Y/%m/%d'): # Change date to string.
    try:
        date_change = datetime.strptime(date_match.group(), fmt)
        date_string0 = date_change.strftime("%Y-%m-%d")
        return(date_string0)
    except:
        print("")

#Download and read html from URL
if __name__ == "__main__":
  cwd=os.path.dirname(__file__)+"/"
  currentfileinfo= file_search("r_*_html_*.txt", cwd ) #Passing pattern and dir
  #print(currentfileinfo)
  #file_web_downloads(".txt")
  count=0
  for url in url_os:

    #file_web_downloads(url)
    urlfile = urllib.request.urlopen(url)
    for line in urlfile:
      decoded = line.decode("utf-8") 
      lowercase_line = decoded.lower()
      if last_change_string in lowercase_line or last_modified_string in lowercase_line:
        string_lower_match=lowercase_line
        newdate=date_find(string_lower_match)
        new_file = cwd+ url_filename[url] + "_" + newdate + ".txt"
        if not(os.path.exists(new_file)):
          urllib.request.urlretrieve(url, new_file)
        count += 1


# Create a method in which you can send the web file name, local file name
# and string to search
# Example
# check_if_file_update(WEBfilename, LOCALfilename, searchSTRING)
# check_if_file_update("https://cran.r-project.org/bin/macosx/, "rmachtml", "last change")

# Add comments to lines that are not self explanatory ( regex line)

# Can improve readability of information by creating a config.txt file which contains the information
# for the files. Can even be a yaml/json file so that if can hold more information
# Example: 
# { windows: 
#     last_updated: 2021-05-20,
#     any_other_extra_info_you_need: EXTRA INFO
# }