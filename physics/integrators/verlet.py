import numpy as np
from config.constants import G
from simulation.body import Body

def compute_acceleration(bodies: list[Body]) -> list[np.ndarray]:
    """
        Computes exact mutual Newtonian gravitational accelerations for all bodies:
        a_i = sum_{j != i} G * m_j * (r_j - r_i) / |r_j - r_i|^3 """
    n = len(bodies)
    accelerations = [np.zeros(3, dtype=np.float64) for _ in range(n)]

    for i in range(n):
        for j in range(i+1,n):
            r_ij = bodies[j].position - bodies[i].position
            dist = np.linalg.norm(r_ij)

            if dist == 0.0:
                continue

            # G/ r^3 scalar factor
            inv_dist_cubed = G / (dist ** 3)

            # equal and opposite forces
            accelerations[i] += inv_dist_cubed * bodies[j].mass * r_ij
            accelerations[j] -= inv_dist_cubed * bodies[i].mass * r_ij
    return accelerations

def step_velocity_verlet(bodies: list[Body], dt:float) -> None:
    """
        Computes exact mutual Newtonian gravitational accelerations for all bodies:
        a_i = sum_{j != i} G * m_j * (r_j - r_i) / |r_j - r_i|^3 """

    # update positions using current velocity and current acceleration
    for body in bodies:
        body.position += body.velocity * dt +0.5 * body.acceleration * (dt **2)

    # evaluate new gravitational accelerations at updated positions
    new_accelerations = compute_acceleration(bodies)

    # update velocities using the average of old and new accelerations
    for body, new_acc in zip(bodies , new_accelerations):
        body.velocity += 0.5 * (body.acceleration + new_acc) * dt
        body.acceleration = new_acc
