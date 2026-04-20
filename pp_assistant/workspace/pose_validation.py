from .workspace import Workspace
from .workspace import Cell, CellSplit


class PoseValidator:
    def __init__(self, workspace: Workspace):
        self. workspace = workspace
    
    def is_point_in_excluded_cell(self, point: tuple[int, int]):
        return self._is_point_in_cell_split(point = point, split = CellSplit.EXCLUDED)

    def is_point_in_eval_cell(self, point: tuple[int, int]):
        return self._is_point_in_cell_split(point = point, split = CellSplit.EVALUATION)
    
    def is_point_in_training_cell(self, point: tuple[int, int]):
        return self. _is_point_in_cell_split(point = point, split = CellSplit.TRAINING)

    def _is_point_in_cell_split(self, point: tuple[int, int], split: CellSplit):
        for cell in self.workspace.cells:
            if not cell.split == split:
                continue

            if self._is_point_in_cell(point = point, cell = cell):
                return True
        
        return False
    

    def _is_point_in_cell(self, point: tuple[int, int], cell: Cell):
        x, y = point
        x_min, y_min = cell.corners[0]
        x_max, y_max = cell.corners[2]

        return x_min <= x <= x_max and y_min <= y <= y_max

