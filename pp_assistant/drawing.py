import cv2
from pp_assistant.workspace.workspace import Workspace
from pp_assistant.workspace.bin import Bin
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

            # Draw bin ID label in top-left corner
            if self.config.drawing.bin_label.show_label:
                bin_label = self.config.drawing.bin_label
                top_left = corners[0]
                
                # Get text size
                text = str(bin.id)
                font = cv2.FONT_HERSHEY_SIMPLEX
                (text_width, text_height), baseline = cv2.getTextSize(
                    text, font, bin_label.font_scale, bin_label.font_thickness
                )
                
                # Calculate background rectangle
                padding = bin_label.bg_padding
                rect_top_left = (
                    top_left[0] + padding,
                    top_left[1] + padding,
                )
                rect_bottom_right = (
                    top_left[0] + padding + text_width + padding,
                    top_left[1] + padding + text_height + baseline + padding,
                )
                
                # Draw background rectangle
                cv2.rectangle(
                    annotated_image,
                    rect_top_left,
                    rect_bottom_right,
                    self.config.drawing.workspace_color,
                    -1,  # Filled rectangle
                )
                
                # Draw text
                text_position = (
                    top_left[0] + 2 * padding,
                    top_left[1] + padding + text_height,
                )
                cv2.putText(
                    annotated_image,
                    text,
                    text_position,
                    font,
                    bin_label.font_scale,
                    (255, 255, 255),  # Black text
                    bin_label.font_thickness,
                )

        return annotated_image
