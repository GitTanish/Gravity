import math
import numpy as np

class Camera3D:
    """ 3D orbit camera with perspective projection"""
    def __init__(self, width: int, height: int, fov: float= 680.0):
        self.width = width
        self.height= height
        self.fov = fov
        self.yaw = 0.42
        self.pitch = 0.58
        self.distance = 112.0
        self.target = np.array([0.0, -4.0, 0.0], dtype=np.float64)


    def project(self, point_3d: np.ndarray) -> tuple[tuple[int, int] | None, float]:
        """projects a 3D point to 2D screen space"""
        p = point_3d - self.target

        # 1. Rotate around Y axis (Yaw)
        cos_y , sin_y = math.cos(self.yaw), math.sin(self.yaw)
        x1 = p[0] * cos_y - p[2] * sin_y
        y1 = p[1]
        z1 = -p[0] * sin_y + p[2] * cos_y

        #2 . Rotate around X axis (Pitch)
        cos_p, sin_p = math.cos(self.pitch), math.sin(self.pitch)
        x2 = x1
        y2 = y1 * cos_p - z1 * sin_p
        z2 = y1 * sin_p + z1 *cos_p + self.distance

        # near plane clipping
        if z2 <= 1.0:
            return None, z2

        sx = int(self.width * 0.5 + (x2/z2)*self.fov)
        sy = int(self.height * 0.5 - (y2/z2)*self.fov)
        return (sx, sy), z2
