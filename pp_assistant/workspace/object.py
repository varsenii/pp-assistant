from .pose import Pose


class Object:

    def __init__(self, id: int, pose: Pose):
        self.id = id
        self.pose = pose