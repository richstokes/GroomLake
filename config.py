import os
import random

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 224
ROAD_WIDTH = 2000  # road width (left to right)
SEGMENT_LENGTH = 100  # segment length (top to bottom)
CAMERA_DEPTH = 1  # camera depth
SHOW_N_SEGMENTS = 300  # number of segments to draw, default 200
LAP_LENGTH = 2700  # length of the lap in segments
F22_APPEAR_AT = 400  # when to show the F22

# Define the colors
DARK_ROAD = 13  # was 4
WHITE_RUMBLE = 7  # was 1
LIGHT_GRASS = 3
DARK_GRASS = 11

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
