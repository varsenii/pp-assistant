import cv2
import numpy as np
import logging
from typing import Tuple


class Rectifier:
    """Handles image rectification and undistortion using camera intrinsics."""

    def __init__(self, intrinsics: np.ndarray, distortion: np.ndarray, frame_size: Tuple[int, int]):
        """
        Initialize the Rectifier with camera calibration parameters.

        Args:
            intrinsics: 3x3 camera intrinsic matrix (K)
            distortion: Distortion coefficients array
            frame_size: (width, height) of the frames to be undistorted
        """
        self.logger = logging.getLogger(__name__)
        self.K = np.array(intrinsics, dtype=np.float64)
        self.dist = np.array(distortion, dtype=np.float64)
        self.frame_size = frame_size
        
        # Precompute optimal camera matrix for efficiency
        self.K_new, _ = cv2.getOptimalNewCameraMatrix(
            self.K, self.dist, frame_size, 1
        )
        
        self.logger.info(
            f"Rectifier initialized with frame size {frame_size}. "
            f"Intrinsics shape: {self.K.shape}, Distortion coeffs: {len(self.dist)}"
        )

    def undistort_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Undistort a single frame using precomputed camera matrix.

        Args:
            frame: The frame to undistort (numpy array)

        Returns:
            The undistorted frame
        """
        return cv2.undistort(frame, self.K, self.dist, None, self.K_new)
