import numpy as np
import cv2
from typing import Iterable, Tuple


class HomographyCalibrator:
    """Computes a homography matrix from world points to image points."""

    def __init__(self, world_points: Iterable[Tuple[float, float]]):
        self.world_points = np.array(world_points, dtype=np.float32)
        self.homography = None

    def compute_homography(self, image_points: Iterable[Tuple[float, float]]) -> np.ndarray:
        image_points_array = np.array(image_points, dtype=np.float32)
        if image_points_array.shape != self.world_points.shape:
            raise ValueError("Image points must have the same shape as world points.")

        self.homography, status = cv2.findHomography(self.world_points, image_points_array)
        if self.homography is None:
            raise RuntimeError("Failed to compute homography from the provided point sets.")
        return self.homography

    def world_to_image(self, x: float, y: float) -> Tuple[int, int]:
        if self.homography is None:
            raise RuntimeError("Homography matrix has not been computed yet.")

        point = np.array([x, y, 1.0], dtype=np.float32)
        projection = self.homography @ point
        return int(projection[0] / projection[2]), int(projection[1] / projection[2])
