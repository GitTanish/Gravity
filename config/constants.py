import numpy as np

# Physical constants using SI units
G = 6.67430e-11  # Gravitational constant 6.67430 x 10^-11 N m^2 kg^-2
M_EARTH = 5.9722e24
M_MOON = 7.3277e22
R_EARTH_MOON = 3.844e8
RADIUS_EARTH = 6.371e6
RADIUS_MOON = 1.737e6

# Simulation Scales
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# 1 second of real time is 2.5 simulated days
TIME_WARP = 86400 * 2.5
PHYSICS_SUBSTEPS = 50
