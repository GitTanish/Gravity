from calendar import c

import pytest
from simulation.orbital_setup import create_earth_moon_system
from config.constants import RADIUS_EARTH

def test_barycenter_is_inside_earth():
    earth, moon, stats = create_earth_moon_system()
    r_bary = stats["r_earth_barycenter_km"] * 1000.0

    # should be around 4681.804 km because no shit sherlock that's what my calculations said
    assert r_bary < RADIUS_EARTH
    assert 4600e3 < r_bary < 4700e3

def test_orbital_period_sidereal():
    earth, moon, stats = create_earth_moon_system()
    period = stats['period_days']

    # must match somewhere around 27.3 days
    assert 27.2 < period < 27.5

def test_net_linear_momentum_is_zero():
    earth, moon, _ = create_earth_moon_system()

    p_earth = earth.mass * earth.velocity
    p_moon = moon.mass * moon.velocity
    p_total = p_earth + p_moon

    scale = max(abs(p_earth).max(), abs(p_moon).max())
    assert abs(p_total).max() <= 1e-14 * scale
