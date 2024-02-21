#!/bin/bash

#####################
# Do not run as root!
#####################

# Install needed packages for the BT
sudo apt install -y dfu-util dfu-programmer gedit

# Same but for python packages
pip install cflib --break-system-packages # This flag is necessary for Python 3.11+, but should not be dangerous

# Init just required submodules for this BT
cd $PAPARAZZI_SRC
git submodule update --init --recursive sw/ext/eigen

################
# Configurations
################

# Flashing to the Crazyflie
sudo usermod -aG dialout $USER

# Configuring the Crazyradio 2.0 USB permissions
sudo groupadd plugdev
sudo usermod -a -G plugdev $USER

cat <<EOF | sudo tee /etc/udev/rules.d/99-bitcraze.rules > /dev/null
# Crazyradio (normal operation)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"
# Bootloader
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", GROUP="plugdev"
# Crazyflie (over USB)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger
