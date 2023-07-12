from offlinedatasci import *
from glob import glob

def test_download_r():
    download_r('testdir')
    assert glob('testdir/R/R-*.pkg')
    assert glob('testdir/R/R-*-win.exe')
