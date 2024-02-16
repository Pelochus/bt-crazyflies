#!/bin/bash

cd paparazzi

# Make Paparazzi GCS AppImage Work
echo "# Needed for Paparazzi AppImage to work" >> /home/$USER/.bashrc
echo "export PAPARAZZI_HOME=$(pwd)" >> /home/$USER/.bashrc
echo "export PAPARAZZI_SRC=$(pwd)" >> /home/$USER/.bashrc

# Get AppImage and move to /usr/bin/pprzgcs so it can be launched by Paparazzi Center
sudo apt install -y wget # Just in case, you should have it anyway
sudo wget https://github.com/paparazzi/PprzGCS/releases/download/v1.0.11/pprzgcs-v1.0.11-x86_64.AppImage -O /usr/bin/pprzgcs
sudo chmod 755 /usr/bin/pprzgcs
