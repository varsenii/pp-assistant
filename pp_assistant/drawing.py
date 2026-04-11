import cv2
from typing import List, Tuple
from pp_assistant.workspace import Workspace


class Drawing:
    """Class responsible for drawing operations on images."""

    def __init__(self, config):
        self.config = config

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
        corners = workspace.corners_img

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