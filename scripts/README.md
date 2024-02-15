## Scripts

These collection of scripts are made to install Paparazzi on Debian 12.
The official guide currently only offers Paparazzi for Ubuntu.

### Quick Install
Run this command:

```bash
wget https://raw.githubusercontent.com/Pelochus/bt-crazyflies/main/scripts/paparazzi-debian-install.sh && sudo bash paparazzi-debian-install.sh
```

### How do these scripts work
The main script ```paparazzi-debian-install.sh``` just calls the other two scripts.
The reason for doing this is purely academic, it better fits a separated explanation of each script for the final thesis report.

#### Paparazzi Center Install
TODO, copy from Appendix A and translate. Explain errors encountered (force jammy PPA) and how they can be improved

#### Paparazzi GCS Install
TODO, copy from Appendix A and translate. Also explain errors (the libproj22 mainly, but also the env situation)
