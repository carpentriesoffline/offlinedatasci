import os
from glob import glob

from offlinedatasci import *

def test_activate_cran(tmp_path, mocker):
    ods_dir = str(tmp_path)
    mocker.patch('os.path.expanduser', return_value=tmp_path)
    activate_cran(ods_dir)
    rprofile_path = Path(os.path.join(tmp_path, ".Rprofile"))
    assert rprofile_path.is_file()
    
    # Check the content of the .Rprofile file
    # with open(rprofile_path) as f:
    #     lines = f.readlines()
    #     assert f'#Added by offlinedatasci' in lines

def test_activate_pypi(tmp_path, mocker):
    ods_dir = str(tmp_path)
    mocker.patch('os.path.expanduser', return_value=ods_dir)
    activate_pypi(ods_dir)

    pip_config_folder_path = Path(os.path.join(tmp_path, ".config", "pip"))
    pip_config_path = Path(pip_config_folder_path, "pip.conf")
    assert pip_config_path.is_file()
    
    with open(pip_config_path) as f:
        lines = f.readlines()
        lines = ''.join(lines)
        assert f"#Added by offlinedatasci" in lines

def test_download_r(tmp_path):
    download_r(tmp_path)
    assert glob(f'{tmp_path}/R/R-*-arm64.pkg')
    assert glob(f'{tmp_path}/R/R-*-x86_64.pkg')
    assert glob(f'{tmp_path}/R/R-*-win.exe')

def test_download_rstudio(tmp_path):    
    download_rstudio(tmp_path)
    assert glob(f"{tmp_path}/rstudio/RStudio-*.dmg")
    assert glob(f"{tmp_path}/rstudio/RStudio-*.exe")

def test_download_python(tmp_path):
    download_python(tmp_path)
    assert glob(f"{tmp_path}/python/python-*.exe")
    assert glob(f"{tmp_path}/python/python-*.pkg")

def test_download_python_libraries(tmp_path):
    # test on notebook since it has caused issues in the past
    # See https://github.com/carpentriesoffline/offlinedatasci/issues/95
    download_python_packages(tmp_path, ['notebook'])
    assert glob(f"{tmp_path}/pythonlibraries/*.whl")
    assert glob(f"{tmp_path}/pypi/index.html")

def test_download_r_packages(tmp_path):
    # test on notebook since it has caused issues in the past
    # See https://github.com/carpentriesoffline/offlinedatasci/issues/95
    download_r_packages(tmp_path, ['RSQLite'])
    assert glob(f"{tmp_path}/miniCRAN/*")

def check_for_empty_folders(folder):
    empty_folders = []
    for root, dirs, files in os.walk(folder):
        if not dirs and not files:
            empty_folders.append(root)
    return empty_folders

def test_download_lessons(tmp_path):
    download_lessons(tmp_path)
    empty_folders = check_for_empty_folders(f"{tmp_path}/lessons")
    assert len(empty_folders) == 0, f"The following folders are empty: {empty_folders}"