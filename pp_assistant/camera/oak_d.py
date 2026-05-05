import depthai as dai
import time
from typing import Tuple
import numpy as np


class DepthAICameraPipeline:
    """Builds and manages a DepthAI pipeline for color camera preview."""

    def __init__(
        self,
        preview_size: Tuple[int, int] = (640, 480),
        interleaved: bool = False,
        stream_name: str = "rgb",
    ):
        self.preview_size = preview_size
        self.interleaved = interleaved
        self.stream_name = stream_name
        self.pipeline = None
        self.device = None
        self.output_queue = None

    def build_pipeline(self) -> None:
        if self.pipeline is not None:
            return  # Already built
        self.pipeline = dai.Pipeline()
        cam = self.pipeline.createColorCamera()
        cam.setPreviewSize(*self.preview_size)
        cam.setInterleaved(self.interleaved)

        xout = self.pipeline.createXLinkOut()
        xout.setStreamName(self.stream_name)
        cam.preview.link(xout.input)
    
    def get_intrinsics(
        self,
        camera_socket: dai.CameraBoardSocket = dai.CameraBoardSocket.CAM_A,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the intrinsic matrix (3x3) and distortion coefficients
        for the requested camera socket of the OAK-D Lite.

        CAM_A = RGB, CAM_B = left mono, CAM_C = right mono.
        """
        with dai.Device() as device:
            calib = device.readCalibration()
            width, height = self.preview_size
            intrinsic_matrix = np.array(
                calib.getCameraIntrinsics(camera_socket, width, height),
                dtype=np.float64,
            )
            dist_coeffs = np.array(
                calib.getDistortionCoefficients(camera_socket),
                dtype=np.float64,
            )
        return intrinsic_matrix, dist_coeffs

    def __enter__(self) -> "DepthAICameraPipeline":
        # Ensure pipeline is built
        self.build_pipeline()
        try:
            self.device = dai.Device(self.pipeline)
        except RuntimeError as e:
            # If device creation fails, try to reset by waiting a bit
            print(f"Device creation failed: {e}. Attempting to reset...")
            time.sleep(2)  # Wait for device to reset
            self.pipeline = None  # Force rebuild
            self.build_pipeline()
            self.device = dai.Device(self.pipeline)
        self.output_queue = self.device.getOutputQueue(self.stream_name, maxSize=4, blocking=False)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.device is not None:
            self.device.close()
            self.device = None
        self.output_queue = None
        # Note: Keep pipeline for potential reuse, but reset if needed

    def get_frame(self):
        if self.output_queue is None:
            raise RuntimeError("Output queue is not initialized. Use the pipeline as a context manager.")
        return self.output_queue.get().getCvFrame()
