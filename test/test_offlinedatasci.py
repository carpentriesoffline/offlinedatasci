from offlinedatasci import *
from glob import glob

def test_download_r(tmp_path):
    download_r(tmp_path)
    assert glob(f'{tmp_path}/R/R-*.pkg')
    assert glob(f'{tmp_path}/R/R-*-win.exe')
