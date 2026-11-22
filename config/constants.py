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

# Visual and 3D camera mapping
SIM_SCALE = 38.0 / R_EARTH_MOON # 384,400 km to 38.0 visual units
GRID_EXTENT = 55.0 # half width of the X-Z potential grid
GRID_STEPS = 44 # number of grid lines along X and Z

# Visual depth scaling for Phi_soft(r) = -sum(G * M / sqrt(r^2 + eps^2))
# Scaled so Earth creates a pronounced, readable funnel without clipping off-screen
POTENTIAL_VISUAL_SCALE = 8.5e-7
SOFTENING_SIM = 1.8
