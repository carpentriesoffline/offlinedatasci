from offlinedatasci import *
from glob import glob
import pytest


@pytest.mark.parametrize("filename", [
    "R-4.4.1-win.exe",
    "R-4.5.12-arm64.pkg",
    "R-4.5.12-x86_64.pkg",
])
def test_find_r_current_version(monkeypatch, filename):
    from offlinedatasci import main

    monkeypatch.setattr(main.requests, "get", lambda url: [
        f'<a href="{filename}">{filename}</a>'.encode("utf-8")
    ])
    assert find_r_current_version("https://example.test/") == filename.rsplit("-", 1)[0]

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
