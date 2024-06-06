# Extracted from:
# https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_swarm_interface/
# To change the URIs:
# https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/#firmware-configuration

import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

def activate_led_bit_mask(scf):
    scf.cf.param.set_value('led.bitmask', 255)

def deactivate_led_bit_mask(scf):
    scf.cf.param.set_value('led.bitmask', 0)

def light_check(scf):
    activate_led_bit_mask(scf)
    time.sleep(2)
    deactivate_led_bit_mask(scf)
    time.sleep(2)

def take_off(scf):
    commander = scf.cf.high_level_commander

    commander.takeoff(1.0, 2.0)
    time.sleep(3)

def land(scf):
    commander = scf.cf.high_level_commander

    commander.land(0.0, 2.0)
    time.sleep(2)

    commander.stop()

def hover_sequence(scf):
    take_off(scf)
    land(scf)

uris = {
    'radio://0/80/2M/E7E7E7E701',
    'radio://0/80/2M/E7E7E7E702',
}

if __name__ == '__main__':
    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        print('Connected to Crazyflies')
        swarm.parallel_safe(light_check)
        swarm.reset_estimators()

        # swarm.sequential(hover_sequence)
        swarm.parallel_safe(hover_sequence)
