import cv2
from typing import Callable, List, Tuple


class PointSelectorUI:
    """Displays an image and collects mouse clicks as image points."""

    def __init__(
        self,
        window_name: str = "image",
        points_required: int = 4,
        callback: Callable[[Tuple[int, int]], None] = None,
    ):
        self.window_name = window_name
        self.points_required = points_required
        self.callback = callback
        self.points: List[Tuple[int, int]] = []

    def _click_handler(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            if self.callback:
                self.callback((x, y))
            print(f"Selected point: {(x, y)}")

    def select_points(self, frame) -> List[Tuple[int, int]]:
        self.points = []
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window_name, self._click_handler)

        while len(self.points) < self.points_required:
            cv2.imshow(self.window_name, frame)
            key = cv2.waitKey(20) & 0xFF
            if key == 27:  # ESC
                break

        cv2.destroyWindow(self.window_name)
        return self.points
