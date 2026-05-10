class Pose:
    def __init__(self, x, y, yaw ):
        self.x = x
        self.y = y
        self.yaw = yaw

    def __repr__(self):
        return f'Pose(x={self.x}, y={self.y}, yaw={self.yaw:.2f})'