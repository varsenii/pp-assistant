import cv2
import logging
import numpy as np
from pp_assistant.camera import DepthAICameraPipeline
from pp_assistant.calibration import HomographyCalibrator
from pp_assistant.config import load_config
from pp_assistant.ui import PointSelectorUI
from pp_assistant.workspace import Workspace
from pp_assistant.drawing import Drawing
from pp_assistant.rectifier import Rectifier


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    config = load_config("pp_assistant/config/config.yaml")

    camera_pipeline = DepthAICameraPipeline(
        preview_size=config.camera.preview_size,
        interleaved=config.camera.interleaved,
        stream_name=config.camera.stream_name,
    )
    camera_pipeline.build_pipeline()

    with camera_pipeline as pipeline:
        frame = pipeline.get_frame()

    # Initialize rectifier for undistortion
    intrinsics = np.array(config.camera.intrinsics, dtype=np.float64)
    distortion = np.array(config.camera.distortion_coeffs, dtype=np.float64)
    logging.info(f"Camera Intrinsics:\n{intrinsics}")
    logging.info(f"Distortion Coefficients:\n{distortion}")
    rectifier = Rectifier(intrinsics, distortion, config.camera.preview_size)
    
    # Undistort the frame
    frame = rectifier.undistort_frame(frame)

    selector = PointSelectorUI(
        window_name=config.ui.window_name,
        points_required=config.ui.points_required,
    )
    image_points = selector.select_points(frame)

    if len(image_points) != config.ui.points_required:
        print(
            f"Expected {config.ui.points_required} points, but got {len(image_points)}."
            " Exiting without computing homography."
        )
        return
    
    workspace = Workspace(config, image_points)
    drawing = Drawing(config)

    calibrator = HomographyCalibrator(world_points=config.calibration.world_points)
    calibrator.compute_homography(image_points)

    u, v = calibrator.world_to_image(*config.calibration.target_world_point)
    annotated_frame = frame.copy()
    cv2.circle(
        annotated_frame,
        (u, v),
        config.marker.radius,
        config.marker.color,
        config.marker.thickness,
    )

    # Draw workspace edges
    annotated_frame = drawing.draw_workspace_edges(annotated_frame, workspace)

    cv2.imshow(config.ui.window_name, annotated_frame)
    print(
        f"Mapped world point {config.calibration.target_world_point} "
        f"to image point {(u, v)}"
    )
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
