#!/bin/bash
cd Offline_Data_Carpentry/scripts/
chmod u+x ./commandscript.sh

#Creating directory for R files if it does not exist
cd ../
echo '$msg1' Creating subdirectory /IBB/Downloads/ if it does not exists. 
echo
mkdir -p ./IBB/Downloads/
echo '$msg2' Calling script to download R and Rstudio files.
echo
python3 scripts/downloadfiles.py

#Downloading Data Carpentry website
echo '$msg3' Calling script to download Data Carpentry website.
./scripts/httrack_carpentries.sh
