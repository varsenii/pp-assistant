class Cell:
    def __init__(self, id, corners):
        self.id = id
        self.corners = corners

    @classmethod
    def from_dict(cls, data: str) -> "Cell":
        return cls(
            id = data.get('id'), 
            corners = data.get('corners')
        )

    def __repr__(self):
        return f"Cell(id={self.id}, corners={len(self.corners)})"