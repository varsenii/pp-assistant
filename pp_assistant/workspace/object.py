import math
import numpy as np
from .pose import Pose


class Object:
    def __init__(self, id: int, pose: Pose, width: float = None, height: float = None):
        self.id = id
        self.pose = pose
        self.width = width
        self.height = height
        self.corners = []

    def _compute_corners(self):
        angle_degrees = math.radians(self.pose.yaw)
        angle_cos = math.cos(angle_degrees)
        angle_sin = math.sin(angle_degrees)

        half_height= self.height / 2
        half_width = self.width / 2

        corners = [
            (half_height, -1 * half_width),
            (half_height, half_width),
            (-1 * half_height, half_width),
            (-1 * half_height, -1 * half_width)
        ]
        
        for x, y in corners:
            xr = x * angle_cos - y * angle_sin
            yr = x * angle_sin + y * angle_cos

            self.corners.append(
                (int(self.pose.x + xr), int(self.pose.y + yr))
            )


        return self.corners if len(self.corners) > 0 else []

    def __repr__(self):
        return f'Pose(id={self.id}), pose={self.pose!r}'