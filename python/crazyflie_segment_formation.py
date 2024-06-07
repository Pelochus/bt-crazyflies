# Made by Pelochus, June 2024

# Base code extracted from:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py
# New modifications inspired by:
# crazyflie_swarm_demo.py
# And my bachelor's thesis

import logging
import time
import threading

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.positioning.motion_commander import MotionCommander

uris = {
    'radio://0/80/2M/E7E7E7E701',
    'radio://0/80/2M/E7E7E7E702',
}

# Only way to access positions easily is making this global (seriously)
all_positions = {}
# Similarly, we need the latest commanded speeds of all drones
all_speeds = {}

DEFAULT_HEIGHT = 0.75
SEGMENT_LIMIT = 1 # This way, it is easier to do the -1 to 1 segment, no need to normalize it
FREQ = 0.25 # How many times we update the speed (and recover current positions) 

# deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

# Calculate the speed
# NOTE: For now, this only works for only two drones!
def kuramoto(my_position, other_positions):
    # First of all, adjust parameters as needed
    k = 1
    desired_offset = 0

    delta = 0
    for position in other_positions:
        delta += position[0] - my_position[0] - desired_offset
    
    return k * delta

def get_xy_from(radio, positions):
    return (positions[radio].x, positions[radio].y)
    
def coordinated_segment(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        while True:
            vnx = all_speeds[scf._link_uri][0]
            vny = all_speeds[scf._link_uri][1] # Currently only 0
            max_vel = 0.5
            
            # First we calculate positions
            print(all_positions)
            my_position = get_xy_from(scf._link_uri, all_positions)

            # Made an array so it can scale in the future
            other_positions = []
            for uri in uris:
                if uri != scf._link_uri:
                    other_positions.append(get_xy_from(uri, all_positions))

            # Now we calculate the extra speed from Kuramoto
            vf = vnx + kuramoto(my_position, other_positions)

            # To limit speed
            if (vf > max_vel):
                vf = max_vel
            elif (vf < -max_vel):
                vf = -max_vel

            if my_position[0] > SEGMENT_LIMIT:
                vnx = -vf
            elif my_position[0] < -SEGMENT_LIMIT:
                vnx = vf

            '''
            if my_position[1] > SEGMENT_LIMIT:
                body_y_cmd = -max_vel
            elif my_position[1] < -SEGMENT_LIMIT:
                body_y_cmd = max_vel
            '''

            all_speeds[scf._link_uri][0] = vnx
            all_speeds[scf._link_uri][1] = vny

            # No yaw, that is why 0 at the end
            mc.start_linear_motion(vnx, vny, 0)
            # TODO Remove here or out
            time.sleep(FREQ)

def recover_positions():
    # Recover positions every t seconds
    global all_positions
    while True:
        all_positions = swarm.get_estimated_positions()
        time.sleep(FREQ / 2) # Update 2 times faster than the speed, just in case

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        print('Connected to Crazyflies!')

        swarm.reset_estimators()
        print("\nEstimators reset! These are the current positions\n")
        print(swarm.get_estimated_positions())
        
        print("\nStarting formation in 3 seconds...\n")
        time.sleep(3)

        # Initialize speed dictionary
        for uri in uris:
            all_speeds[uri] = [0.25, 0] # x, y respectively

        # Run threads
        recover_positions_thread = threading.Thread(target=recover_positions)
        recover_positions_thread.start()
        time.sleep(0.01) # So that the previous thread has some time to update the variable the first time
        swarm.parallel_safe(coordinated_segment)
        recover_positions_thread.join()