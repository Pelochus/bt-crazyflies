# Made by Pelochus, June 2024
# This experiment proves that my thesis works

import logging
import time
import threading

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

i = 1
waiting_iter = 15 # How much shall the second drone wait: 1 s = 5 iterations (since each iteration = 200 ms)
max_iterations = 1
positions = {}
sim_speed = [0, 0]

# Note: I've found that the real nominal speed of the real log is around 0.12 m/s, even though 0.25 was commanded.
# At least that's why it is by it's estimated positions
NOMINAL_SPEED = [0.1, 0] # x, y respectively
SEGMENT_LIMIT = 0.5
FREQ = 0.2 # Seconds till we update the speed

FILE_PATH = "./log.txt"

# Calculate the speed
# NOTE: For now, this only works for only two drones!
def kuramoto():
    # First of all, adjust parameters as needed
    k = 0.24
    desired_offset = 0
    delta = 0

    delta += positions['real'][0] - positions['sim'][0] - desired_offset
    
    return k * delta
    
def coordinated_segment():
    global i

    # Get the real drone position
    positions['real'][0] = get_number_from_line(FILE_PATH, i)
    i += 1

    # Now calculate simulated drone speed and its position ONLY if waited enough
    if (i > waiting_iter):
        # Change direction if passed the limit, also change direction of nominal speed
        if (positions['sim'][0] > SEGMENT_LIMIT):
            sim_speed[0] = -NOMINAL_SPEED[0]
        elif (positions['sim'][0] < -SEGMENT_LIMIT):
            sim_speed[0] = NOMINAL_SPEED[0]
        else: # Reset speed, we don't want cumulative adding kuramoto()
            if sim_speed[0] < 0:
                sim_speed[0] = -NOMINAL_SPEED[0]
            elif sim_speed[0] > 0:
                sim_speed[0] = NOMINAL_SPEED[0]

        # Add Kuramoto extra speed
        sim_speed[0] += kuramoto()

        # Based on that speed, what would be the next position in FREQ seconds?
        positions['sim'][0] += sim_speed[0] * FREQ

        print("Position: ", positions['sim'][0])
        print("Speed: ", sim_speed[0])

def get_number_from_line(file_path, line_number):
    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                try:
                    # Convert line to number
                    number = float(line.strip())
                    return number
                except ValueError:
                    print(f"Error: Couldn't convert line {line_number} to a number.")
                    return None
        print(f"Error: Line {line_number} not found.")
        return None

if __name__ == '__main__':
    with open(FILE_PATH, 'r') as file:
        lines = file.readlines()
        max_iterations = len(lines) # How many iterations, which is exactly how many lines are in the real drone log

    # Y is fixed
    positions['real'] = [0, 0.5]
    positions['sim'] = [0, -0.5]

    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    # Horizontal line y = 0
    ax.axhline(0, color='g', linestyle='--', linewidth=2)

    # Vertical -1 and 1 lines
    ax.axvline(0.5, color='g', linestyle='--', linewidth=2)
    ax.axvline(-0.5, color='g', linestyle='--', linewidth=2)

    # Initialize positions
    real_drone_position, = ax.plot([], [], 'bo')  # 'bo' is blue point
    sim_drone_position, = ax.plot([], [], 'ro')  # 'ro' is red point

    def init():
        real_drone_position.set_data([], [])
        sim_drone_position.set_data([], [])
        return real_drone_position, sim_drone_position

    # Update positions
    def update(frame):
        coordinated_segment() # Calculate positions
        real_drone_position.set_data(positions['real'][0], positions['real'][1])
        sim_drone_position.set_data(positions['sim'][0], positions['sim'][1])
        return real_drone_position, sim_drone_position

    ani = FuncAnimation(fig, update, frames=np.arange(0, 100), init_func=init, blit=True, interval=(FREQ * 1000))
    plt.show()
