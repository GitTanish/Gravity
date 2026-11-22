import numpy as np
import pygame
from config.constants import SIM_SCALE
from field.potential_grid import PotentialGrid
from simulation.body import Body
from visualization.camera import Camera3D

class Renderer:
    """Renders the 3D potential mesh, celestial bodies, trails, and diagnostics HUD."""

    def __init__(self, screen:pygame.Surface, camera: Camera3D):
        self.screen = screen
        self.camera = camera
        self.font = pygame.font.SysFont("monospace", 14)
        self.font_bold = pygame.font.SysFont("monospace",15, bold=True)

        # visual overrides in pixels so Earth and Moon remain clearly visible
        self.visual_radii = {"Earth":12, "Moon":5}

    def render(self, bodies: list[Body], grid:PotentialGrid, telemetry: dict, show_grid: bool = True)-> None:
        self.screen.fill((8,11,18))

        # Render 3d gravitational potential grid
        if show_grid:
            self._draw_potential_grid(grid)
        # Render barycenter origin marker (0,0,0)
        barry_pt, _ = self.camera.project(np.array([0.0,0.0,0.0]))
        if barry_pt:
            bx, by = barry_pt
            pygame.draw.line(self.screen, (130,140,160),(bx-6,by), (bx+6, by),1)
            pygame.draw.line(self.screen, (130,140,160),(bx,by-6), (bx, by+6),1)
            lbl = self.font.render("Barycenter", True, (130,140,160))
            self.screen.blit(lbl, (bx+8, by-7))

        # render orbital trails
        for body in bodies:
            if len(body.trail)>1:
                pts = []
                for pos in body.trail:
                    pt3 = np.array([pos[0]*SIM_SCALE, 0.0, pos[2]* SIM_SCALE])
                    proj, _ = self.camera.project(pt3)
                    if proj:
                        pts.append(proj)
                if len(pts)>1:
                    pygame.draw.lines(self.screen, body.color, False, pts,1)

        # render depth-sorted bodies
        draw_queue = []
        for body in bodies:
            sx= body.position[0]* SIM_SCALE
            sz= body.position[2]* SIM_SCALE
            sy = grid.compute_height_at_point(sx, sz, bodies) if show_grid else 0.0

            proj, depth = self.camera.project(np.array([sx,sy,sz]))
            if proj:
                rad = self.visual_radii.get(body.name, 6)
                draw_queue.append((depth, body.name, proj, body.color, rad))

        # painter's algorithm: draw farthest objects first
        draw_queue.sort(key=lambda item: item[0], reverse=True)
        for _, name, pt, color, rad in draw_queue:
            pygame.draw.circle(self.screen, color, pt,rad)
            pygame.draw.circle(self.screen,(255,255,255),pt,rad, 1)
            tag = self.font.render(name, True, (215, 225, 240))
            self.screen.blit(tag, (pt[0]+ rad + 5, pt[1]-7))

        # render telemetry hud
        self._draw_hud(telemetry)

    def _draw_potential_grid(self, grid: PotentialGrid)-> None:
        steps = grid.steps
        projected = {}

        for r in range(steps):
            for c in range(steps):
                pt3 = np.array([grid.grid_x[r,c], grid.grid_y[r,c], grid.grid_z[r,c]])
                projected[(r,c)], _ = self.camera.project(pt3)

        grid_color = (26,48, 88)
        for r in range(steps):
            row = [projected[(r,c)] for c in range(steps) if projected[(r,c)] is not None]
            if len(row)>1:
                pygame.draw.lines(self.screen, grid_color, False, row, 1)

        for c in range(steps):
            col = [projected[(r,c)] for r in range(steps) if projected[(r,c)] is not None]
            if len(col)>1:
                pygame.draw.lines(self.screen, grid_color, False, col, 1)

    def _draw_hud(self, t: dict) -> None:
            status = "PAUSED" if t["paused"] else "RUNNING"
            lines = [
                (f"elapsed Time: {t['days']:6.2f} days [{status}]", (110, 240, 140)),
                (f"earth-Moon Distance: {t['distance_km']:,.1f} km", (230, 235, 245)),
                (f"total Energy (E): {t['energy']:.5e} J (Drift: {t['energy_drift']:.2e})", (230, 235, 245)),
                (f"angular Momentum |L|: {t['angular_momentum']:.5e} kg*m^2/s", (200, 210, 230)),
                ("[Mouse Drag] Orbit Camera | [Scroll] Zoom | [G] Toggle Grid | [SPACE] Pause", (120, 135, 160)),
            ]
            for idx, (text, color) in enumerate(lines):
                surf = self.font_bold.render(text, True, color) if idx == 0 else self.font.render(text, True, color)
                self.screen.blit(surf, (18, 16 + idx * 22))
