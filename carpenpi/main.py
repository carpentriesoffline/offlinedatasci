#Creating directory for R files if it does not exist
# Download files using download files.py
#Downloading Data Carpentry website using httrack

import wget
from pathlib import Path

def create_carpenpi_dir(directory='~/carpenpi'):
    folder_path = Path(directory)
    if not folder_path.exists():
        print("\nCreating carpenpi folder in " + directory)
        Path.mkdir(folder_path, parents=True)
