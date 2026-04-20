from enum import Enum, auto
from typing import Iterable, Tuple


class CellSplit(str, Enum):
    TRAINING = 'training'
    EVALUATION = 'evaluation'
    EXCLUDED = 'excluded'


class Cell:
    def __init__(self, id: int, corners = Iterable[Tuple[float, float]], split: CellSplit = None):
        self.id = id
        self.corners = corners
        self.split = split

    @classmethod
    def from_dict(cls, data: str) -> "Cell":
        return cls(
            id = data.get('id'), 
            corners = data.get('corners'),
            split = data.get('split')
        )