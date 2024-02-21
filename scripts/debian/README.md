## Debian Scripts

These collection of scripts are made to install Paparazzi on Debian 12.
The official guide currently only offers Paparazzi for Ubuntu.

### Quick Install
Run this command on the directory you want Paparazzi source to be downloaded.
Your ```sudo``` password will be asked:

```bash
wget https://raw.githubusercontent.com/Pelochus/bt-crazyflies/main/scripts/debian/paparazzi-debian-install.sh && bash paparazzi-debian-install.sh
```

**NOTE: Do not execute this command as sudo unless you want your /root/.bashrc modified instead of your user.**

### Extended installation
Run in the root of the Paparazzi source if you want all libraries (may not be necessary): 

```bash
git submodule update --init --recursive .
```

### How do these scripts work
The main script ```paparazzi-debian-install.sh``` just calls the other two scripts.
The reason for doing this is purely academic, it better fits a separated explanation of each script for the final thesis report

#### Paparazzi Center Install
The script works this way:

- Forces the PPA repos for Ubuntu with ```[trusted=yes]``` and telling the repos to use the ```jammy``` version
- Install all packages except ```pprzgcs``` since it needs libproj22 for installing

#### Paparazzi GCS Install
This script uses the official AppImage to substitute the broken Ubuntu package for Paparazzi GCS:

- Set the environment variables ```PAPARAZZI_HOME``` and ```PAPARAZZI_GCS``` in ```.bashrc``` to where the source code is downloaded. The AppImage needs this to work
- Download the AppImage with wget and move it as ```/usr/bin/pprzgcs```. Give exec permissions

### Useful Links
- Official guide: https://paparazzi-uav.readthedocs.io/en/latest/quickstart/install.html
- GCS official repo: https://github.com/paparazzi/PprzGCS/
- Force unsigned repo: https://askubuntu.com/questions/732985/force-update-from-unsigned-repository
- PPA: https://launchpad.net/~paparazzi-uav/+archive/ubuntu/ppa?field.series_filter=jammy
