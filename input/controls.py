import math
import pygame
from visualization.camera import Camera3D

class InputHandler:
    """Manages mouse camera orbiting, scroll zooming, and simulation hotkeys."""

    def __init__(self, camera: Camera3D):
        self.camera= camera
        self.dragging = False
        self.last_mouse = (0,0)
        self.paused = False
        self.show_grid = True
        self.running = True

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_r:
                    # reset camera to default view
                    self.camera.yaw = 0.42
                    self.camera.pitch = 0.58
                    self.camera.distance = 112.0

            elif event.type == pygame.MOUSEWHEEL:
                self.camera.distance = max(35.0, min(240.0, self.camera.distance - event.y * 5.0))

            # click and drag
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.dragging = True
                self.last_mouse = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                dx = event.pos[0]-self.last_mouse[0]
                dy = event.pos[1]-self.last_mouse[1]
                self.camera.yaw += dx * 0.006
                self.camera.pitch = max(0.05, min(math.pi * 0.48, self.camera.pitch +dy * 0.006))
                self.last_mouse = event.pos

            # continuous keyboard camera controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.camera.yaw -= 0.03
            if keys[pygame.K_RIGHT] or keys[pygame.K_w]:
                self.camera.pitch = min(math.pi * 0.48, self.camera.pitch + 0.025)
            if keys[pygame.K_UP] or keys[pygame.K_s]:
                self.camera.pitch = max(0.05, self.camera.pitch - 0.025)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.camera.pitch = max(0.05, self.camera.pitch - 0.025)
            if keys[pygame.K_EQUALS] or keys[pygame.K_e]:
                self.camera.distance = max(35.0, self.camera.distance - 1.5)
            if keys[pygame.K_MINUS] or keys[pygame.K_q]:
                self.camera.distance = min(240.0, self.camera.distance + 1.5)
