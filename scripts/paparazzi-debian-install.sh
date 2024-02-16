#!/bin/bash

sudo apt install -y wget # Just in case

# Get files
wget https://raw.githubusercontent.com/Pelochus/bt-crazyflies/main/scripts/paparazzi-center-install.sh
wget https://raw.githubusercontent.com/Pelochus/bt-crazyflies/main/scripts/paparazzi-gcs-install.sh

# Give them permissions
sudo chmod 755 ./paparazzi-center-install.sh
sudo chmod 755 ./paparazzi-gcs-install.sh

# Run each different script
sudo /bin/bash ./paparazzi-center-install.sh
sudo /bin/bash ./paparazzi-gcs-install.sh

# Remove (now) unnecesary files
rm -f ./paparazzi-center-install.sh
rm -f ./paparazzi-gcs-install.sh

# Run!
# ./paparazzi
