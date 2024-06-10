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
current_speed = {}

NOMINAL_SPEED = {}
DESIRED_X_SPEED = 0.33
DESIRED_Y_SPEED = 0
DEFAULT_HEIGHT = 0.75
SEGMENT_LIMIT = 1 # This way, it is easier to do the -1 to 1 segment, no need to normalize it
FREQ = 0.2 # How many times we update the speed

# deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

# Calculate the speed
# NOTE: For now, this only works for only two drones!
def kuramoto(my_position, other_positions):
    # First of all, adjust parameters as needed
    k = 0.1
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
            # First we calculate positions
            my_position = get_xy_from(scf._link_uri, all_positions)

            # Made it an array so it can scale in the future
            other_positions = []
            for uri in uris:
                if uri != scf._link_uri:
                    other_positions.append(get_xy_from(uri, all_positions))

            global NOMINAL_SPEED
            # Change direction if passed the limit, also change direction of nominal speed
            if my_position[0] > SEGMENT_LIMIT:
                NOMINAL_SPEED[scf._link_uri][0] *= -1
            elif my_position[0] < -SEGMENT_LIMIT:
                NOMINAL_SPEED[scf._link_uri][0] *= -1

            # Get nominal (desired standard) speeds in x and y
            vnx = NOMINAL_SPEED[scf._link_uri][0]
            vny = NOMINAL_SPEED[scf._link_uri][1] # Currently 0
            max_vel = 0.5

            # TODO: Same for Y axis

            # Now we calculate the extra speed from Kuramoto, with the correct nominal speed
            vnx += kuramoto(my_position, other_positions)

            # Limit speed TODO: Is this necessary, anyway?
            '''
            if (vf > max_vel):
                vf = max_vel
            elif (vf < -max_vel):
                vf = -max_vel
            '''

            # Not needed, left just in case for future improvements
            current_speed[scf._link_uri][0] = vnx
            current_speed[scf._link_uri][1] = vny

            print("I'm: ", scf._link_uri, " with X: ", my_position[0], " and with Vx: ", vnx)

            # No yaw, that is why 0 at the end
            mc.start_linear_motion(vnx, vny, 0)
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

        # Initialize all current and nominal speeds
        for uri in uris:
            current_speed[uri] = [0.25, 0] # x, y respectively
            NOMINAL_SPEED[uri] = [DESIRED_X_SPEED, DESIRED_Y_SPEED] # x, y respectively

        # Run threads
        recover_positions_thread = threading.Thread(target=recover_positions)
        
        recover_positions_thread.start()
        time.sleep(0.01) # So that the previous thread has some time to update the variable the first time
        swarm.parallel_safe(coordinated_segment)
        
        recover_positions_thread.join()