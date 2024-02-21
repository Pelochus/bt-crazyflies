#!/bin/bash

sudo apt update && sudo apt full-upgrade -y

# In order to add the Ubuntu PPA, I followed this guide
# The Debian repos are dead, only way is to force a PPA repo in Debian
# https://linuxconfig.org/install-packages-from-an-ubuntu-ppa-on-debian-linux
sudo apt install -y build-essential devscripts

# Important note: [trusted=yes] is not recommended, is better to add the pubkeys according to the tutorial
# I have not done it because I am lazy to understand how I can change apt-key to gpg command
# https://askubuntu.com/questions/732985/force-update-from-unsigned-repository
echo "deb [trusted=yes] https://ppa.launchpadcontent.net/paparazzi-uav/ppa/ubuntu jammy main" | sudo tee -a /etc/apt/sources.list
echo "deb-src [trusted=yes] https://ppa.launchpadcontent.net/paparazzi-uav/ppa/ubuntu jammy main" | sudo tee -a /etc/apt/sources.list

# Rest of the official Paparazzi guide
# https://paparazzi-uav.readthedocs.io/en/latest/quickstart/install.html
sudo apt update
sudo apt install -y paparazzi-dev gcc-arm-none-eabi gdb-multiarch paparazzi-jsbsim dfu-util python-is-python3

# Clone Paparazzi
git clone --origin upstream https://github.com/paparazzi/paparazzi.git
cd paparazzi
git checkout v6.3 # Currently last stable version

# Compile latest stable
make

# TODO: Try to put paparazzi in /usr/bin with a symlink so it can be globally executed

# Run!
# ./paparazzi
