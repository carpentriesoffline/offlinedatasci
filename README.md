# Web free data science

Tools for teaching and doing data science without an internet connection

## Status

Early stage experiment

## Getting started

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
