import logging
import numpy as np
from typing import Iterable, Tuple

from pp_assistant.workspace.cell import Cell

class Workspace:
    def __init__(self, corners_world, corners_img: Iterable[Tuple[int, int]], cells: list[Cell] = None, ):
        self.logger = logging.getLogger(__name__)
        self.corners_world = corners_world
        self.corners_img = corners_img
        self.cells = cells

    @classmethod
    def from_dict(cls, data) -> 'Workspace':
        return cls(
            corners_world = data.get('corners_world'), 
            corners_img = data.get('corners_img'),
            cells = [Cell.from_dict(data = cell) for cell in data.get('cells')]
        )
    
    def to_dict(self) -> dict[str, tuple]:
        return {
            'corners_world': self.corners_world,
            'corners_img': self.corners_img,
            'cells': [cell.__dict__ for cell in self.cells]
        }

    def compute_cells(self, n_rows, n_cols) -> list[Cell]:
        top_left, top_right, bottom_right, bottom_left = self.corners_world

        min_x = min(top_left[0], bottom_left[0])
        max_x = max(top_right[0], bottom_right[0])
        min_y = min(top_left[1], top_right[1])
        max_y = max(bottom_left[1], bottom_right[1])
        x_coordinates = np.linspace(min_x, max_x, num=n_cols+1)
        y_coordinates = np.linspace(min_y, max_y, num=n_rows+1)
        
        n_cells = n_rows * n_cols

        cells = []
        for i in range(n_cells):
            idx_x = i % n_cols
            idx_y = i // n_cols
            cell_top_left = (x_coordinates[idx_x], y_coordinates[idx_y])
            cell_top_right = (x_coordinates[idx_x + 1], y_coordinates[idx_y])
            cell_bottom_right = (x_coordinates[idx_x + 1], y_coordinates[idx_y + 1])
            cell_bottom_left = (x_coordinates[idx_x], y_coordinates[idx_y + 1])

            cell = Cell(id=i, corners=[cell_top_left, cell_top_right, cell_bottom_right, cell_bottom_left])

            cells.append(cell)
        
        self.cells = cells