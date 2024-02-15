#!/bin/bash

################################
# PLEASE RUN THIS SCRIPT AS SUDO
################################

# Make Paparazzi GCS AppImage Work
echo "# Needed for Paparazzi AppImage to work" >> /home/$USER/.bashrc
echo "export PAPARAZZI_HOME=$(pwd)" >> /home/$USER/.bashrc
echo "export PAPARAZZI_SRC=$(pwd)" >> /home/$USER/.bashrc

# Get AppImage
sudo apt install -y wget # Just in case, you should have it anyway
wget https://github.com/paparazzi/PprzGCS/releases/download/v1.0.11/pprzgcs-v1.0.11-x86_64.AppImage -O pprzgcs-v1.0.11.AppImage
sudo chmod 755 pprzgcs-v1.0.11.AppImage

# Make sure Paparazzi can search the AppImage
# TODO
