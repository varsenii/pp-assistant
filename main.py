import cv2
import logging
import numpy as np
import argparse
import os

from pp_assistant.camera.oak_d import DepthAICameraPipeline
from pp_assistant.calibration import HomographyCalibrator
from pp_assistant.config import load_config
from pp_assistant.ui import PointSelectorUI
from pp_assistant.workspace.workspace import Workspace
from pp_assistant.dataset import Dataset
from pp_assistant.drawing import Drawing
from pp_assistant.rectifier import Rectifier
from pp_assistant.workspace.object import Object
from pp_assistant.interaction import UserPrompter
from pp_assistant.workspace.sampling import PoeSampler


def parse_args():
    parser = argparse.ArgumentParser(description="PP Assistant - pick-and-place data collection tool")

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Name of the dataset",
    )

    return parser.parse_args()


def main(dataset_name: str) -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
    config = load_config("pp_assistant/config/config.yaml")

    dataset_dir = os.path.join(config.dataset.base_path, dataset_name)

    try:
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
        logging.debug(f"Camera Intrinsics:\n{intrinsics}")
        logging.debug(f"Distortion Coefficients:\n{distortion}")
        rectifier = Rectifier(intrinsics, distortion, config.camera.preview_size)
        
        # Undistort the frame
        frame = rectifier.undistort_frame(frame)
        
        is_dataset_loaded = False
        # Load the dataset if exists
        if os.path.exists(dataset_dir):
            logging.info(f"Existing dataset found at {dataset_dir}. Loading workspace corners.")
            dataset = Dataset.from_json(path = dataset_dir)
            is_dataset_loaded = True
        
        # Use UI to select workspace corners
        else:            
            logging.info("No existing dataset found. Starting workspace selection.")
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
            
            prompter = UserPrompter()
            n_rows, n_cols = prompter.ask_workspace_grid()

            workspace = Workspace(config.calibration.world_points, image_points)
            workspace.compute_cells(n_rows = n_rows, n_cols = n_cols)

            dataset = Dataset(name=dataset_name, workspace=workspace)
            dataset.save(dataset_dir)


        calibrator = HomographyCalibrator(world_points=config.calibration.world_points)
        calibrator.compute_homography(dataset.workspace.corners_img)

        drawing = Drawing(config, calibrator = calibrator)

        # Draw workspace
        annotated_frame = frame.copy()
        annotated_frame = drawing.draw_workspace_edges(annotated_frame, dataset.workspace)
        annotated_frame = drawing.draw_cels(annotated_frame, dataset.workspace.cells)

        # Sample object poses
        pose_sampler = PoeSampler(workspace = dataset.workspace)

        # Draw object poses incrementally every 0.5 seconds
        objects = pose_sampler.sobol_sample(num_samples = 100, num_objects = 3)
        for object in objects:
            annotated_frame = drawing.draw_object(annotated_frame, object)
            cv2.imshow(config.ui.window_name, annotated_frame)
            
            key = cv2.waitKey(100)
            if key != -1:
                break

        # Ask the excluded and evaluation cells
        if not is_dataset_loaded:
            cell_ids = prompter.ask_excluded_cells()
            dataset.workspace.mark_excluded_cells(ids = cell_ids)

            cell_ids = prompter.ask_evaluation_cells()
            dataset.workspace.mark_evaluation_cells(ids = cell_ids)
            dataset.save(dataset_dir)

        
    except Exception as e:
        logging.exception(str(e))
    finally:
        logging.info('Destroying windows...')
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    args = parse_args()
    main(args.dataset)
