import logging
import math
from typing import Iterable, List, Tuple

class Workspace:
    def __init__(self, corners_world, corners_img: Iterable[Tuple[int, int]]):
        self.logger = logging.getLogger(__name__)
        self.corners_world = corners_world
        self.corners_img = self._compute_corners(list(corners_img))

    def _compute_corners(self, points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if len(points) != 4:
            raise ValueError("Workspace corners must contain exactly 4 points.")

        ordered_corners = self._order_corners_clockwise(points)
        self.logger.info(f"Workspace corners set to: {ordered_corners}")
        return ordered_corners

    def _order_corners_clockwise(self, points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        center_x = sum(p[0] for p in points) / len(points)
        center_y = sum(p[1] for p in points) / len(points)
        sorted_points = sorted(
            points,
            key=lambda p: math.atan2(p[1] - center_y, p[0] - center_x),
        )

        # Rotate so the first point is the top-left corner
        top_left_index = min(range(4), key=lambda i: (sorted_points[i][1], sorted_points[i][0]))
        return [tuple(sorted_points[(top_left_index + i) % 4]) for i in range(4)]
    
    def to_dict(self) -> 'Workspace':
        return {
            'corners_world': self.corners_world,
            'corners_img': self.corners_img
        }

