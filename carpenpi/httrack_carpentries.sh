#!/bin/bash
chmod u+x /scripts/httrack_carpentries.sh

#Using HTTRACK to download files
#-W asks for link specific actions
#Test
httrack https://datacarpentry.org/spreadsheet-ecology-lesson/00-intro/index.html -O ./IBB/Data_Carpentry

#Asking per each url course of action
#httrack https://datacarpentry.org/spreadsheet-ecology-lesson/00-intro/index.html -O /home/pi/IBB/Data_Carpentry -W