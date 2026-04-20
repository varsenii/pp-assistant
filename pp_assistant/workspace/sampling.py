import numpy as np
import logging
from scipy.stats import qmc

from .pose import Pose
from .pose_validation import PoseValidator
from .workspace import Workspace
from .object import Object


class PoeSampler:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.max_x = self.workspace.corners_world[1][0]
        self.max_y = self.workspace.corners_world[3][1]
        self.logger = logging.getLogger(__name__)
        self.pose_validator = PoseValidator(workspace = self.workspace)
    
    def uniform_sample(self, num_samples) -> list[Pose]:
        x_samples = np.random.uniform(low = 0, high = self.max_x, size = num_samples)
        y_samples = np.random.uniform(low = 0, high = self.max_y, size = num_samples)
        yaw_samples = np.random.uniform(low = 0, high = 360, size = num_samples)

        return [
            Pose(x = x, y = y, yaw = yaw) for (x, y, yaw) in zip(x_samples, y_samples, yaw_samples)
        ]

    def stratified_sample(self, resolution: int) -> list[Pose]:
        self.logger.info(f"Stratified sampling for each {resolution} quadratic cm...")
        num_samples_x = int(self.max_x // resolution)
        num_samples_y = int(self.max_y // resolution)
        num_samples = num_samples_x * num_samples_y
        self.logger.info(f'Sampling {num_samples} poses')

        x_samples = np.linspace(start = 0, stop = self.max_x, num = num_samples_x + 1)
        y_samples = np.linspace(start = 0, stop = self.max_y, num = num_samples_y + 1)

        poses = []
        for i in range(num_samples_x):
            for j in range(num_samples_y):
                x = np.random.uniform(x_samples[i], x_samples[i + 1])
                y = np.random.uniform(y_samples[j], y_samples[j + 1])
                yaw = np.random.uniform(0, 360, 1)
                poses.append(Pose(x = x, y = y, yaw = yaw))
        
        return poses
    
    def sobol_sample(self, num_samples, num_objects) -> list[Object]:
        batch_size = max(64, num_samples)
        valid_samples = []

        while len(valid_samples) < num_samples:
            sampler = qmc.Sobol(d=4, scramble=True)
            samples_raw = sampler.random(batch_size)

            # scale to your bounds
            l_bounds = [0, 0, 0, 0]
            u_bounds = [self.max_x, self.max_y, 360, num_objects + 1]
            samples = qmc.scale(samples_raw, l_bounds, u_bounds)

            # Filter invalid poses
            for sample in samples:
                position = (sample[0], sample[1])
                if not self.pose_validator.is_point_in_training_cell(position):
                    continue

                valid_samples.append(sample)

                if len(valid_samples) >= num_samples:
                    break

        return [
            Object(
                id = int(np.round(id)),
                pose = Pose(x = x, y = y, yaw = yaw)
            ) 
            for x, y, yaw, id in valid_samples
        ]

        