import numpy as np

class Body:
    def __init__(self, name:str, mass:float, radius : float,
                 position:np.ndarray, velocity:np.ndarray, color: tuple):

                     self.name =name
                     self.mass = float(mass)
                     self.radius = float(radius)

                     # 3d vectors: [x, y, z]
                     self.position = np.array(position, dtype=np.float64)
                     self.velocity = np.array(velocity, dtype=np.float64)
                     self.acceleration = np.zeros(3, dtype=np.float64)
                     self.color = color
                     self.trail = []

    def record_trial(self, max_points: int = 400):
        self.trail.append(self.position.copy())
        if len(self.trail)> max_points:
            self.trail.pop(0)
