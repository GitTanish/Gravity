import sys
import numpy as np
import pygame

from config.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TIME_WARP, PHYSICS_SUBSTEPS
from simulation.orbital_setup import create_earth_moon_system
from physics.integrators.verlet import compute_acceleration, step_velocity_verlet
from physics.diagnostics import compute_total_energy, compute_angular_momentum
from field.potential_grid import PotentialGrid
from visualization.camera import Camera3D
from visualization.renderer import Renderer
from input.controls import InputHandler

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Earth Moon Gravity and Spacetime Curvature Simulation")
    clock = pygame.time.Clock()

    # initialize earth moon system and initial accelerations
    earth, moon, _ = create_earth_moon_system()
    bodies = [earth, moon]

    for body, acc in zip(bodies, compute_acceleration(bodies)):
        body.acceleration = acc

    _, _, initial_energy = compute_total_energy(bodies)
    sim_time_sec = 0.0

    # initialize field, camera , renderer and input handler
    potential_grid = PotentialGrid()
    camera = Camera3D(WINDOW_WIDTH, WINDOW_HEIGHT)
    renderer = Renderer(screen, camera)
    controls = InputHandler(camera)

    # main simulation loop
    while controls.running:
        dt_real = clock.tick() / 1000.0
        controls.process_events()

        if not controls.paused:
            dt_sim = (TIME_WARP * dt_real)/PHYSICS_SUBSTEPS
            for _ in range(PHYSICS_SUBSTEPS):
                step_velocity_verlet(bodies, dt_sim)
                sim_time_sec += dt_sim

            for body in bodies:
                body.record_trial(max_points=350)

        # update scalar gravitational potential mesh
        if controls.show_grid:
            potential_grid.update(bodies)

        # compute live physical invariants from HUD
        _, _, current_energy = compute_total_energy(bodies)
        l_vec = compute_angular_momentum(bodies)
        distance_m = float(np.linalg.norm(moon.position - earth.position))

        telemetry = {
            "days": sim_time_sec/ 86400.0,
            "distance_km":distance_m/1000.0,
            "energy": current_energy,
            "energy_drift":abs(current_energy - initial_energy)/abs(initial_energy),
            "angular_momentum": float(np.linalg.norm(l_vec)),
            "paused": controls.paused,
        }

        renderer.render(bodies, potential_grid, telemetry, show_grid = controls.show_grid)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
