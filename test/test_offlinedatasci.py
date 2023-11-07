from offlinedatasci import *
from glob import glob

def test_download_r():
    download_r('testdir')
    assert glob('testdir/R/R-*.pkg')
    assert glob('testdir/R/R-*-win.exe')

def test_download_rstudio(tmp_path):    
    download_rstudio(tmp_path)
    assert glob(f"{tmp_path}/rstudio/RStudio-*.dmg")
    assert glob(f"{tmp_path}/rstudio/RStudio-*.exe")

def test_download_python(tmp_path):
    download_python(tmp_path)
    assert glob(f"{tmp_path}/python/python-*.exe")
    assert glob(f"{tmp_path}/python/python-*.pkg")

def test_download_lessons():
    captured = download_lessons("testdir").readouterr()
    assert "This is a test output." in captured.out
    files_in_current_directory = glob(os.path.join("tmp_path", '*'))
    files_in_current_directory = glob(os.path.join("testdir/", '*'))
    files_in_current_directory = ["testdir/datacarpentry.org","testdir/swcarpentry.github.io" ]
    print("names of subfolders are:", files_in_current_directory)
    results = []
    all_file_names = []
    for folder_names in files_in_current_directory:
        folder_path = os.path.join('.', folder_names)
        all_file_names.append(folder_names)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files = glob(os.path.join(folder_path, '*'))
            if len(files) >= 2:
                results.append(True) 
            else:
                results.append(False)     
        else:
            print(f"{folder_names}: Folder not found")
            results.append(False) 
    print("names of files being checked:", all_file_names)
    print(results)
    #for folder_name in glob.glob(f"{tmp_path}/python"):
    #Create list with lesson files in name.py
    #test
