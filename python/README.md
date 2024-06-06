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

### crazyflie_segment_formation.py
Uses 2 Crazyflies in parallel running in parallel segments with GVF.
Then, an algorithm coordinates them so that the move next to each other in their corresponding segment.

More info (Spanish only) in the "Capítulo 4" of my bachelor's thesis:

TODO PUT LINK
