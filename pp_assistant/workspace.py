import logging
import math
from typing import Iterable, List, Tuple

class Workspace:
    def __init__(self, corners_world, corners_img: Iterable[Tuple[int, int]]):
        self.logger = logging.getLogger(__name__)
        self.corners_world = corners_world
        self.corners_img = corners_img


    @classmethod
    def from_dict(cls, data) -> 'Workspace':
        return cls(
            corners_world = data.get('corners_world'), 
            corners_img = data.get('corners_img')
        )
    
    def to_dict(self) -> dict[str, tuple]:
        return {
            'corners_world': self.corners_world,
            'corners_img': self.corners_img
        }

