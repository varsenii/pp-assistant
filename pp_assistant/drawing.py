import cv2
from pp_assistant.workspace.workspace import Workspace
from pp_assistant.bin import Bin
from pp_assistant.calibration import HomographyCalibrator


class Drawing:
    """Class responsible for drawing operations on images."""

    def __init__(self, config, calibrator: HomographyCalibrator):
        self.config = config
        self.calibrator = calibrator

    def draw_workspace_edges(self, image, workspace: Workspace):
        """
        Draws the edges of the workspace's rectangular shape on the given image.

        Args:
            image: The image to draw on (numpy array).
            workspace: The Workspace object containing the corners.

        Returns:
            The annotated image.
        """
        annotated_image = image.copy()
        corners =  workspace.corners_img
        
        # Draw lines between consecutive corners
        for i in range(len(corners)):
            start_point = corners[i]
            end_point = corners[(i + 1) % len(corners)]  # Wrap around to first point
            cv2.line(
                annotated_image,
                start_point,
                end_point,
                self.config.drawing.workspace_color,
                self.config.drawing.workspace_thickness,
            )

        return annotated_image

    def draw_bins(self, image, bins: list[Bin]):
        annotated_image = image.copy()

        for bin in bins:
            corners = [
                self.calibrator.world_to_image(*coordinates) for coordinates in bin.corners
            ]

            # Draw lines between consecutive corners
            for i in range(len(corners)):
                start_point = corners[i]
                end_point = corners[(i + 1) % len(corners)]  # Wrap around to first point
                cv2.line(
                    annotated_image,
                    start_point,
                    end_point,
                    self.config.drawing.workspace_color,
                    self.config.drawing.workspace_thickness,
                )

        return annotated_image
