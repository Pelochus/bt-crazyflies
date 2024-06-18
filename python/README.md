## Python files for control and coordination
Files for controlling one or more Crazyflie with their official firmware

### crazyflie_demo.py
Take-off, move 0.5m forward, move 0.5 backwards and land.
Needs Flow Deck v2 and Crazyradio.

More info:
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_motion_commander/

### crazyflie_swarm_demo.py
Take-off and land, with some LEDs flashing.
Needs Crazyradio and changing the URIs of the involved Crazyflies so they are not the same one.

More info:
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_swarm_interface/

Changing the URIs:
https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/#firmware-configuration

### crazyflie_single_segment.py
Based off the `crazyflie_demo.py`, it is pretty much the same but follows a segment indefinitely.
Try it out before going into `crazyflie_segment_formation.py` to make sure it follows segment decently.
It also shows the estimated position. 

### crazyflie_segment_formation.py
Uses 2 Crazyflies in parallel running in parallel segments with GVF.
Then, an algorithm coordinates them so that the move next to each other in their corresponding segment.

More info (Spanish only) in the "Capítulo 4" of my bachelor's thesis:
TODO PUT LINK

### sim and lighthouse folders
The first one contains a graphical experiment made for my thesis,
with one log from a real drone and a simulated drone using the algorithm developed for this thesis.

The lighthouse folder has modified files from this folder adapted for the Lighthouse Positioning System.
It ended up in failures, so I advise against using it as is.

### Useful Links
- https://github.com/bitcraze/crazyflie-lib-python/tree/master/examples
- https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/high_level_commander/
- https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/commander/
- https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/localization/
- https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/swarm/
