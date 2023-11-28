import os
import random

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 224
roadW = 2000  # road width (left to right)
segL = 100  # segment length (top to bottom)
camD = 1  # camera depth
show_N_seg = 300  # number of segments to draw, default 200
LAP_LENGTH = 2700  # length of the lap in segments
F22_APPEAR_AT = 400  # when to show the F22

# Define the map size and angle
x_map = 50
y_map = 60
angle_map = 0

# Define line length and angle increment
length_map = 1

# Define the colors
dark_road = 13  # was 4
white_rumble = 7  # was 1
light_grass = 3
dark_grass = 11

# properties for use with the track generation
# Random values for curves
# Define mean and standard deviation for normal distribution
mu = 0  # Mean
sigma = 0.8  # Standard deviation (controls the spread of values)

# Generate random values using normal distribution
CORNER_RAND_VALUE_1 = random.gauss(mu, sigma)
CORNER_RAND_VALUE_2 = random.gauss(mu, sigma * 1.2)
CORNER_RAND_VALUE_3 = random.gauss(mu, sigma * 1.4)
CORNER_RAND_VALUE_4 = random.gauss(mu, sigma)

# Random values for distance between curves
DISTANCE_RAND_VALUE_1 = random.randint(100, 200)
DISTANCE_RAND_VALUE_2 = random.randint(100, 400)
DISTANCE_RAND_VALUE_3 = random.randint(200, 600)
DISTANCE_RAND_VALUE_4 = random.randint(200, 800)


# toggle debug info
DEBUG_MODE = True
if os.environ.get("DEBUG") == "1":
    DEBUG_MODE = True
else:
    DEBUG_MODE = False
