## Dependencies Scripts

These collection of scripts are dependencies for the making of this Bachelor's Thesis.

### Quick Install
You should already have installed Paparazzi. If on Debian you can follow this [guide](https://github.com/Pelochus/bt-crazyflies/tree/main/scripts/debian#Quick-Install).

Run this command for installing the dependencies on Debian. You should run this script within the Paparazzi source folder.
May also work with derivatives like Ubuntu.
Your ```sudo``` password will be asked:

```bash
wget https://raw.githubusercontent.com/Pelochus/bt-crazyflies/main/scripts/deps/deps-install.sh && bash deps-install.sh
```

### What is installed
This script install the following packages:
- dfu-util
- dfu-programmer

It also inits the submodule for Eigen, needed for this Bachelor's Thesis. Not needed if already inited all submodules:

```bash
# If in the Paparazzi source folder
git submodule update --init --recursive sw/ext/eigen
```

### Useful Links
- Flashing firmware on Crazyflie: https://wiki.paparazziuav.org/wiki/Crazyflie_2.0
