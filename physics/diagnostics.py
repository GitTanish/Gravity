import numpy as np
from config.constants import G
from simulation.body import Body

def compute_kinetic_energy(bodies: list[Body]) -> float:
    """K = sum(0.5 * m_i * |v_i|^2)"""
    return sum(0.5 * b.mass * float(np.dot(b.velocity, b.velocity)) for b in bodies)

def compute_potential_energy(bodies: list[Body]) -> float:
    """U = -sum_{i < j} (G * m_i * m_j / |r_j - r_i|)"""
    u_total = 0.0
    n = len(bodies)
    for i in range(n):
        for j in range(i+1, n):
            dist = float(np.linalg.norm(bodies[j].position - bodies[i].position))
            if dist > 0.0:
                u_total -= (G * bodies[i].mass * bodies[j].mass)/dist
    return u_total

def compute_total_energy(bodies: list[Body]) -> tuple[float, float, float]:
    """Returns (K, U, E = K + U) in Joules."""
    k = compute_kinetic_energy(bodies)
    u = compute_potential_energy(bodies)
    return k, u, k+ u

def compute_angular_momentum(bodies: list[Body]) -> np.ndarray:
    """L = sum(r_i x (m_i * v_i)) in kg * m^2 / s."""
    l_total = np.zeros(3, dtype=np.float64)
    for b in bodies:
        l_total += np.cross(b.position , b.mass * b.velocity)
    return l_total
