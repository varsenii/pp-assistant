from ..workspace.object import Object


class Episode:
    def __init__(self, id: int, objects: list[Object]):
        self.id = id
        self.objects = objects