#!/bin/bash

# Install needed packages for the BT
sudo apt install -y dfu-util dfu-programmer gedit

# Init just required submodules for this BT
cd $PAPARAZZI_SRC
git submodule update --init --recursive sw/ext/eigen
