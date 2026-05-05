import cv2
import logging
import math

from pp_assistant.workspace.workspace import Workspace
from pp_assistant.workspace.cell import Cell
from pp_assistant.calibration import HomographyCalibrator
from pp_assistant.workspace.pose import Pose
from pp_assistant.workspace.object import Object


class Drawing:
    """Class responsible for drawing operations on images."""

    def __init__(self, config, calibrator: HomographyCalibrator):
        self.config = config
        self.calibrator = calibrator
        self.logger = logging.getLogger(__name__)

    def draw_workspace_edges(self, image, workspace: Workspace):
        """
        Draws the edges of the workspace's rectangular shape on the given image.

        Args:
            image: The image to draw on (numpy array).
            workspace: The Workspace object containing the corners.

        Returns:
            The annotated image.
        """
        corners =  workspace.corners_img
        
        # Draw lines between consecutive corners
        for i in range(len(corners)):
            start_point = corners[i]
            end_point = corners[(i + 1) % len(corners)]  # Wrap around to first point
            cv2.line(
                image,
                start_point,
                end_point,
                self.config.drawing.workspace_color,
                self.config.drawing.workspace_thickness,
            )

        return image

    def draw_cels(self, image, cells: list[Cell]):
        for cell in cells:
            corners = [
                self.calibrator.world_to_image(*coordinates) for coordinates in cell.corners
            ]

            # Draw lines between consecutive corners
            for i in range(len(corners)):
                start_point = corners[i]
                end_point = corners[(i + 1) % len(corners)]  # Wrap around to first point
                cv2.line(
                    image,
                    start_point,
                    end_point,
                    self.config.drawing.workspace_color,
                    self.config.drawing.workspace_thickness,
                )

            # Draw cell ID label in top-left corner
            if self.config.drawing.cell_label.show_label:
                cell_label = self.config.drawing.cell_label
                top_left = corners[0]
                
                # Get text size
                text = str(cell.id)
                font = cv2.FONT_HERSHEY_SIMPLEX
                (text_width, text_height), baseline = cv2.getTextSize(
                    text, font, cell_label.font_scale, cell_label.font_thickness
                )
                
                # Calculate background rectangle
                padding = cell_label.bg_padding
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
                    image,
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
                    image,
                    text,
                    text_position,
                    font,
                    cell_label.font_scale,
                    (255, 255, 255),  # Black text
                    cell_label.font_thickness,
                )

        return image
    

    def draw_objects(self, image, objects:list[Object]):
        for object in objects:
            image = self.draw_object(image = image, object = object)
        return image
    

    def draw_object(self, image, object: Object):
        pose = object.pose
        color = self.config.marker.color

        for obj_config in self.config.objects.objects:
            if obj_config.id == object.id:
                color = obj_config.color
                break

        u, v = self.calibrator.world_to_image(pose.x, pose.y)
        cv2.circle(
            image,
            (u, v),
            self.config.marker.radius,
            color,
            self.config.marker.thickness,
        )
        
        # Draw yaw as a small arrow
        arrow_length = 10
        end_u = int(u + arrow_length * math.cos(pose.yaw))
        end_v = int(v + arrow_length * math.sin(pose.yaw))
        cv2.arrowedLine(
            image,
            (u, v),
            (end_u, end_v),
            color,
            2,
        )
    
        return image
