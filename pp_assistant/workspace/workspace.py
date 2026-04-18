import logging
import numpy as np
from typing import Iterable, Tuple

from pp_assistant.bin import Bin

class Workspace:
    def __init__(self, corners_world, corners_img: Iterable[Tuple[int, int]], bins: list[Bin] = None, ):
        self.logger = logging.getLogger(__name__)
        self.corners_world = corners_world
        self.corners_img = corners_img
        self.bins = bins

    @classmethod
    def from_dict(cls, data) -> 'Workspace':
        return cls(
            corners_world = data.get('corners_world'), 
            corners_img = data.get('corners_img'),
            bins = [Bin.from_dict(data = bin) for bin in data.get('bins')]
        )
    
    def to_dict(self) -> dict[str, tuple]:
        return {
            'corners_world': self.corners_world,
            'corners_img': self.corners_img,
            'bins': [bin.__dict__ for bin in self.bins]
        }

    def compute_bins(self, n_rows, n_cols) -> list[Bin]:
        top_left, top_right, bottom_right, bottom_left = self.corners_world

        min_x = min(top_left[0], bottom_left[0])
        max_x = max(top_right[0], bottom_right[0])
        min_y = min(top_left[1], top_right[1])
        max_y = max(bottom_left[1], bottom_right[1])
        x_coordinates = np.linspace(min_x, max_x, num=n_cols+1)
        y_coordinates = np.linspace(min_y, max_y, num=n_rows+1)
        
        n_bins = n_rows * n_cols

        bins = []
        for i in range(n_bins):
            idx_x = i % n_cols
            idx_y = i % n_rows
            bin_top_left = (x_coordinates[idx_x], y_coordinates[idx_y])
            bin_top_right = (x_coordinates[idx_x + 1], y_coordinates[idx_y])
            bin_bottom_right = (x_coordinates[idx_x + 1], y_coordinates[idx_y + 1])
            bin_bottom_left = (x_coordinates[idx_x], y_coordinates[idx_y + 1])

            bin = Bin(id=i, corners=[bin_top_left, bin_top_right, bin_bottom_right, bin_bottom_left])

            bins.append(bin)
        
        self.bins = bins