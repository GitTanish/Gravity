import numpy as np
from config.constants import (
    G,
    SIM_SCALE,
    GRID_EXTENT,
    GRID_STEPS,
    POTENTIAL_VISUAL_SCALE,
    SOFTENING_SIM,
)

from simulation.body import Body

class PotentialGrid:
    """Computes the 3D height field y(x, z) from the scalar gravitational potential Phi."""
    def __init__(self, extent:float =GRID_EXTENT, steps: int = GRID_STEPS):
        self.steps = steps
        axis = np.linspace(-extent, extent, steps , dtype=np.float64)
        self.grid_x, self.grid_z = np.meshgrid(axis, axis)
        self.grid_y = np.zeros_like(self.grid_x)

    def compute_height_at_point(self, sim_x: float, sim_z:float, bodies:list[Body]):
        """Evaluates softened potential height at a single (x, z) coordinate in visual units."""
        total_y = 0.0
        for body in bodies:
            bx = body.position[0]* SIM_SCALE
            bz = body.position[2]* SIM_SCALE
            dist_soft = np.hypot(sim_x - bx, sim_z - bz)
            dist_soft = np.sqrt(dist_soft**2 + SOFTENING_SIM**2)
            phi = -(G * body.mass) / (dist_soft/SIM_SCALE)
            total_y += phi * POTENTIAL_VISUAL_SCALE
        return float(total_y)

    def update(self, bodies:list[Body]) -> None:
        """Vectorized evaluation of Phi_soft(r) across all grid vertices."""
        self.grid_y.fill(0.0)
        for body in bodies:
            bx = body.position[0]* SIM_SCALE
            bz = body.position[2]* SIM_SCALE

            dx= self.grid_x -bx
            dz = self.grid_z - bz
            r_soft_meters = np.sqrt(dx**2 + dz**2 + SOFTENING_SIM**2)/ SIM_SCALE

            # scalar potential superposition: Phi(r) = -sum(G * m_i / r_i)
            phi = -(G * body.mass)/ r_soft_meters
            self.grid_y += phi * POTENTIAL_VISUAL_SCALE
