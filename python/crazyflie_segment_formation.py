# Made by Pelochus, June 2024

# Base code extracted from:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py
# New modifications inspired by:
# crazyflie_swarm_demo.py
# And my bachelor's thesis

import logging
import time
from threading import Event
from collections import namedtuple # May be necessary, check

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

uris = {
    'radio://0/80/2M/E7E7E7E701',
    'radio://0/80/2M/E7E7E7E702',
}

all_positions = {}

DEFAULT_HEIGHT = 0.75
SEGMENT_LIMIT = 1 # This way, it is easier to do the -1 to 1 segment.

# deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

# Calculate the desired extra speed 
def kuramoto():
    # TODO
    pass

def get_xy_from(radio, positions):
    print(positions)
    # return (positions[radio].x, positions[radio].y)

def prueba(scf):
    print("Hello, I am ", scf._link_uri)
    print(all_positions)
    for position in all_positions:
        print(position)
    # get_xy_from(scf._link_uri, positions)
    # position_estimate = get_xy_from(scf._link_uri, positions)
    # print(position_estimate)
    
def move_segment_limit(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        body_x_cmd = 0.15
        body_y_cmd = 0.0
        max_vel = 0.3

        while (1):
            # First we calculate our positions
            position_estimate = get_xy_from(scf._link_uri, all_positions)

            if position_estimate[0] > SEGMENT_LIMIT:
                body_x_cmd = -max_vel
            elif position_estimate[0] < -SEGMENT_LIMIT:
                body_x_cmd = max_vel

            '''
            if position_estimate[1] > SEGMENT_LIMIT:
                body_y_cmd = -max_vel
            elif position_estimate[1] < -SEGMENT_LIMIT:
                body_y_cmd = max_vel
            '''

            # No yaw, that is why 0 at the end
            mc.start_linear_motion(body_x_cmd, body_y_cmd, 0)
            time.sleep(0.1)

# Horrible solution to pass the estimated positions of both drones to both drones
# There is no other way I've found, since the wrapper only passes the positions
# to its corresponding drone if it finds the URI as a key in the dictionary
# and we need the positions of all drones for each drone
# At least it should work for N drones
def make_positions_dict(positions):
    param = {}
    for uri in uris:
        param[uri] = positions

    # For making sure it works
    # for p in param.items():
        # print(p)

    return param

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        print('Connected to Crazyflies!')
        
        # I believe this is not needed, but will leave it as a reminder if things do not work
        # Remember to add the function param_deck_flow back if needed (from crazyflie_demo.py)

        # swarm.cf.param.add_update_callback(group='deck', name='bcFlow2', cb=param_deck_flow)
        # if not deck_attached_event.wait(timeout=5):
            # print('No flow deck detected!')
            # sys.exit(1)

        swarm.reset_estimators()
        print("\nEstimators reset! These are the current positions\n")
        print(swarm.get_estimated_positions())
        
        print("\nStarting formation in 1 second...\n")
        time.sleep(1)

        # Recover positions every frequency seconds
        frequency = 0.5
        while True:
            # pos_dict = make_positions_dict(swarm.get_estimated_positions())
            all_positions = swarm.get_estimated_positions()
            swarm.parallel_safe(prueba)
            # swarm.parallel_safe(move_segment_limit, swarm.get_estimated_positions())
            time.sleep(frequency)