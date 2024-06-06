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

DEFAULT_HEIGHT = 0.75
SEGMENT_LIMIT = 1 # This way, it is easier to do the -1 to 1 segment.

# deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

# Calculate the desired extra speed 
def kuramoto():
    # TODO
    pass

def my_position(radio, positions):
    resultados = {}
    positions = swarm.get_estimated_positions()

    for radio in uris:
        if radio == positions:
            position = positions[radio]
            resultados[radio] = {'x': position.x, 'y': position.y}
            return resultados
        else:
            resultados[radio] = {'x': None, 'y': None}
    return resultados

def prueba(scf, positions):
    position_estimate = my_position(scf._link_uri, positions)
    print(position_estimate)
    
def move_segment_limit(scf, swarm):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        body_x_cmd = 0.15
        body_y_cmd = 0.0
        max_vel = 0.3

        while (1):
            # First we calculate our positions
            position_estimate = my_position(scf._link_uri, swarm)

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
        # Need to fix, cant pass swarm nor swarm.get_positions to this function...
        swarm.parallel_safe(prueba, swarm)
        # swarm.parallel_safe(move_segment_limit, swarm.get_estimated_positions())