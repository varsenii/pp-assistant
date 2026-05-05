import numpy as np
import logging
from scipy.stats import qmc

from .pose import Pose
from .pose_validation import PoseValidator
from .workspace import Workspace
from .object import Object
from ..dataset.episode import Episode


class EpisodeGenerator:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.max_x = self.workspace.corners_world[1][0]
        self.max_y = self.workspace.corners_world[3][1]
        self.logger = logging.getLogger(__name__)
        self.pose_validator = PoseValidator(workspace=self.workspace)

    def generate_episodes(
        self,
        num_episodes: int,
        max_num_objects: int,
        min_num_objects: int = 1,
    ) -> list[Episode]:
        if min_num_objects < 1:
            raise ValueError("min_num_objects must be at least 1.")
        if min_num_objects > max_num_objects:
            raise ValueError("min_num_objects cannot exceed max_num_objects.")

        episodes = []
        for i in range(num_episodes):
            num_objects = np.random.randint(min_num_objects, max_num_objects + 1)
            objects = self._generate_objects(num_objects=num_objects, max_num_objects=max_num_objects)
            episodes.append(Episode(id=i, objects=objects))

        return episodes

    def _generate_objects(self, num_objects: int, max_num_objects: int) -> list[Object]:
        # Sample unique IDs up front — Sobol is unsuitable for discrete unique values
        object_ids = np.random.choice(max_num_objects, size=num_objects, replace=False)

        poses = self._sample_valid_poses(num_objects)

        return [
            Object(id=int(object_id), pose=Pose(x=x, y=y, yaw=yaw))
            for object_id, (x, y, yaw) in zip(object_ids, poses)
        ]

    def _sample_valid_poses(self, num_poses: int) -> list[tuple[float, float, float]]:
        """Sample valid (x, y, yaw) poses using a Sobol sequence."""
        batch_size = max(64, num_poses * 2)  # Oversample to account for filtered-out poses
        valid_poses = []

        l_bounds = [0,        0,        0]
        u_bounds = [self.max_x, self.max_y, 360]

        while len(valid_poses) < num_poses:
            sampler = qmc.Sobol(d=3, scramble=True)  # 3 dimensions: (x, y, yaw)
            samples = qmc.scale(sampler.random(batch_size), l_bounds, u_bounds)

            for x, y, yaw in samples:
                if not self.pose_validator.is_point_in_training_cell((x, y)):
                    continue

                valid_poses.append((x, y, yaw))

                if len(valid_poses) >= num_poses:
                    break

        return valid_poses