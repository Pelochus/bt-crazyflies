# Made by Pelochus, June 2024

# Base code extracted from:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py
# New modifications inspired in: from crazyflie_swarm_demo.py
# And my bachelor's thesis

import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Remember to change the URI accordingly (if needed)
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E702')

uris = {
    'radio://0/80/2M/E7E7E7E701',
    'radio://0/80/2M/E7E7E7E702',
}

DEFAULT_HEIGHT = 0.5
SEGMENT_LIMIT = 1

deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

def move_segment_limit(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        body_x_cmd = 0.15
        body_y_cmd = 0.0
        max_vel = 0.3

        while (1):
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

            mc.start_linear_motion(body_x_cmd, body_y_cmd, 0)
            time.sleep(0.1)

def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)

    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        print('Connected to Crazyflies')
        # swarm.cf.param.add_update_callback(group='deck', name='bcFlow2', cb=param_deck_flow)
        swarm.reset_estimators()

        # if not deck_attached_event.wait(timeout=5):
            # print('No flow deck detected!')
            # sys.exit(1)

        print(swarm.get_estimated_positions())