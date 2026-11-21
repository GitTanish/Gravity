# tests/test_conservation.py
import numpy as np
from simulation.orbital_setup import create_earth_moon_system
from physics.integrators.verlet import compute_acceleration, step_velocity_verlet
from physics.diagnostics import (
    compute_total_energy,
    compute_angular_momentum,
)

def test_virial_theorem_initial():
    earth, moon, _ = create_earth_moon_system()
    bodies = [earth, moon]
    k, u, e = compute_total_energy(bodies)

    # For a circular orbit: K = -0.5 * U, and E = 0.5 * U
    assert np.isclose(k, -0.5 * u, rtol=1e-12)
    assert np.isclose(e, 0.5 * u, rtol=1e-12)

def test_energy_and_angular_momentum_conservation_full_orbit():
    earth, moon, stats = create_earth_moon_system()
    bodies = [earth, moon]

    # Initialize a(0)
    accs = compute_acceleration(bodies)
    for b, a in zip(bodies, accs):
        b.acceleration = a

    _, _, e_initial = compute_total_energy(bodies)
    l_initial = compute_angular_momentum(bodies)

    # Simulate 1 full orbital period (~27.28 days) with dt = 60 seconds
    period_sec = stats["period_days"] * 86400.0
    dt = 60.0
    steps = int(period_sec / dt)

    for _ in range(steps):
        step_velocity_verlet(bodies, dt)

    _, _, e_final = compute_total_energy(bodies)
    l_final = compute_angular_momentum(bodies)

    # Relative energy drift must be practically zero (< 1e-11)
    rel_energy_error = abs(e_final - e_initial) / abs(e_initial)
    assert rel_energy_error < 1e-11

    # Angular momentum vector must be conserved
    assert np.allclose(l_final, l_initial, rtol=1e-11)
