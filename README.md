# Web free data science

Tools for teaching and doing data science without an internet connection

## Status

Early stage experiment

## Installation

### From the repository:

Clone the repository and from the root directory run:

```sh
pip install .
```

### From GitHub:

```sh
pip install git+https://git@github.com/weecology/web-free-data-science.git
```

## Usage

### Download carpenpi files

From the command line run:

```sh
carpenpi download /path/to/download/to
```


## Original instructors for setting up Raspberry Pi (being replaced by new carpenpi stack)

### Buy and setup a Raspberry Pi 4

1. Get a Raspberry Pi 4 (current testing uses the 4GB model)
2. If the Raspberry Pi comes with NOOBS (many do)
    1. [Download a new Raspbian image](https://www.raspberrypi.org/downloads/raspbian/)
    2. [Download and install balenaEtcher](https://www.balena.io/etcher/)
    3. Use balenaEtcher to flash the Raspbain image onto your Raspberry Pi's memory card. *This requires a memory card reader, which may have come with your Raspberry Pi or may need to be purchased separately.
3. Boot up your Raspberry Pi and run the following from the terminal
    1. `sudo apt update`
    2. `sudo apt upgrade`

### Install Internet in a Box

Install [Internet in a Box](https://github.com/iiab/iiab) using the one-line install script

1. The installation will take about an hour
2. It is recommend that you use an ethernet cable for internet connectivity if possible
    1. If you do install over wifi you need to "run `iiab-hotspot-on` after IIAB installation"
    2. See details at [iiab's install site](http://download.iiab.io/)
3. You will be asked a number of questions during the install script
4. In general the default choices are good
5. It is not necessary to edit the config file initially
6. When asked to choose the size of the install choose the smallest option (this is fastests and what has currently been tested)
7. OK, now you're ready. Tun the installer from the terminal
8. `curl d.iiab.io/install.txt | sudo bash`
9. Follow the instructions on the screen as you go. You may have to restart several times and restart the installation processes following the instructions provided on the screen.

### Check that the installation works

1. On a computer, tablet, or smartphone open the available wifi networks and see if `Internet in a Box` is available
2. Connect to this network
3. Open a browser
4. Navigate to `http://box`
5. If you see a mobile site for Internet in a Box everything worked

### Setting up a local CRAN or partial CRAN mirror

#### Partial CRAN mirror

1. Install the R package [miniCRAN](https://github.com/andrie/miniCRAN)
2. Create a local CRAN mirror that contains all of your desired packages and their dependencies.
   The following example installs `tidyverse` and all of its dependencies, but you can add more
   packages to the `pkgs` line to expand this. Replace `/path` with where you want to
   store the CRAN mirror. Currently this should be an external harddrive.

```
library(miniCRAN)
repo <- "https://cran.rstudio.com"
pkgs <- c("tidyverse")
pkgList <- pkgDep(pkgs, repos=repo, type="source", suggests=FALSE)
makeRepo(pkgList, path="/path", repos=repo,
         type=c("source", "win.binary", "mac.binary.el-capitan"))
```

#### Full CRAN mirror

1. Follow [official instructions](https://cran.r-project.org/mirror-howto.html) (expansion of these instructions welcome, just haven't done it yet)
2. This is ~1/4 TB so make sure that you have a large enough external harddrive

#### Adding the CRAN mirror to the Raspberry Pi

1. Attach the external harddrive to your Raspberry Pi and restart
2. The files should now be available at http://box/usb/usb0/path where `path` is the path on the external harddrive
