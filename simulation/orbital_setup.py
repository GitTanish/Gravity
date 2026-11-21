import math
import numpy as np
from config.constants import G, M_EARTH, M_MOON, R_EARTH_MOON, RADIUS_EARTH, RADIUS_MOON
from simulation.body import Body

def create_earth_moon_system() -> tuple[Body, Body, dict]:
    """ Initializes Earth and Moon in the circular orbits around their shared barycenter.
    Positions and velocities lie on the X-Z plane (Y is normal/depth).
    """
    # 1 BaryCenter offsets (two body mechanics and the barycenter)
    m_total = M_EARTH + M_MOON
    r_earth = (M_MOON/ m_total) * R_EARTH_MOON
    r_moon = (M_EARTH/ m_total) * R_EARTH_MOON

    # 2 oRbital Mechanics and kepler's third law
    # omega^2 = G * M_total / R^3
    omega = math.sqrt((G * m_total) / (R_EARTH_MOON ** 3))
    t_period = 2.0 * math.pi / omega # seconds

    # 3 Tangential velocities
    v_earth = omega * r_earth
    v_moon = omega * r_moon

    # Positions on X-axis, velocities along +Z / -Z (XZ plane)
    pos_earth = np.array([-r_earth, 0.0, 0.0], dtype=np.float64)
    vel_earth = np.array([0.0, 0.0, -v_earth], dtype=np.float64)

    pos_moon = np.array([r_moon, 0.0, 0.0], dtype = np.float64)
    vel_moon = np.array([0.0, 0.0, v_moon], dtype=np.float64)

    earth = Body("Earth", M_EARTH, RADIUS_EARTH, pos_earth, vel_earth,(70, 160, 255))
    moon = Body("Moon",M_MOON, RADIUS_MOON, pos_moon, vel_moon, (215,215, 225))

    stats = {
        "r_earth_barycenter_km": r_earth/1000.0,
        "r_moon_barycenter_km": r_moon/1000.0,
        "period_days": t_period/ 86400.0,
        "v_earth_mps": v_earth,
        "v_moon_mps": v_moon,
    }

    return earth, moon, stats
