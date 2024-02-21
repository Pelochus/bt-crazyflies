## Dependencies Scripts
These collection of scripts are dependencies and configurations for the making of this Bachelor's Thesis.

### Quick Install
You should already have installed Paparazzi. If on Debian you can follow this [guide](https://github.com/Pelochus/bt-crazyflies/tree/main/scripts/debian#Quick-Install).

Run this command for installing the dependencies on Debian. You should run this script within the Paparazzi source folder.
May also work with derivatives like Ubuntu.
Your ```sudo``` password will be asked:

```bash
wget https://raw.githubusercontent.com/Pelochus/bt-crazyflies/main/scripts/deps/deps-install.sh && bash deps-install.sh
```

**NOTE: Similar to Debian installation scripts, should not be run as sudo unless you want it installed for root user**

### What is installed/configured
This script install the following packages:
- dfu-util
- dfu-programmer
- gedit
- cflib (with pip)

DFU packages are needed for flashing the firmware to the Crazyflies.
gedit is used as default editor for Paparazzi.
cflib is a library needed for communication with the Crazyflie using the Crazyradio 2.0. It is forced for Python 3.11+ installations

It also inits the submodule for Eigen, needed for this Bachelor's Thesis. Not needed if already inited all submodules:

```bash
# If in the Paparazzi source folder
git submodule update --init --recursive sw/ext/eigen
```

For configurations:
- Adds the current user to the group dialout
- Configures the Crazyradio 2.0 USB permissions

### Useful Links
- Flashing firmware on Crazyflie: https://wiki.paparazziuav.org/wiki/Crazyflie_2.0
- Make Crazyradio 2.0 work: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/
- cflib installation: https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/installation/install.md
