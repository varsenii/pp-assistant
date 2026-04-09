import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


def _normalize_tuple(value: Sequence[Any], expected_length: int) -> Tuple[Any, ...]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"Expected a list or tuple, got {type(value).__name__}")
    if len(value) != expected_length:
        raise ValueError(f"Expected {expected_length} values, got {len(value)}")
    return tuple(value)


def _normalize_point_list(value: Sequence[Sequence[float]]) -> List[Tuple[float, float]]:
    return [tuple(point) for point in value]


@dataclass
class CameraConfig:
    preview_size: Tuple[int, int] = (640, 480)
    interleaved: bool = False
    stream_name: str = "rgb"
    intrinsics: List[List[float]] = field(default_factory=lambda: [[500.38571167, 0.0, 314.06344604], [0.0, 500.47668457, 238.7240448], [0.0, 0.0, 1.0]])
    distortion_coeffs: List[float] = field(default_factory=lambda: [-4.14610481e+00, 1.10561991e+01, -3.34565295e-04, -5.48989163e-04, -7.81179380e+00, -4.22761488e+00, 1.13181620e+01, -8.09042549e+00, 0.0, 0.0, 0.0, 0.0, -7.13373360e-04, -1.07512390e-03])


@dataclass
class UIConfig:
    window_name: str = "image"
    points_required: int = 4


@dataclass
class CalibrationConfig:
    world_points: List[Tuple[float, float]] = field(
        default_factory=lambda: [
            (0.0, 0.0),
            (10.0, 0.0),
            (10.0, 10.0),
            (0.0, 10.0),
        ]
    )
    target_world_point: Tuple[float, float] = (1.0, 1.0)


@dataclass
class MarkerConfig:
    color: Tuple[int, int, int] = (0, 0, 255)
    radius: int = 5
    thickness: int = -1


@dataclass
class DrawingConfig:
    workspace_color: Tuple[int, int, int] = (255, 0, 0)
    workspace_thickness: int = 2


@dataclass
class AppConfig:
    camera: CameraConfig = field(default_factory=CameraConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    calibration: CalibrationConfig = field(default_factory=CalibrationConfig)
    marker: MarkerConfig = field(default_factory=MarkerConfig)
    drawing: DrawingConfig = field(default_factory=DrawingConfig)


def load_config(file_path: str = "config.yaml") -> AppConfig:
    config_path = Path(file_path)
    if not config_path.exists():
        return AppConfig()

    with config_path.open("r", encoding="utf-8") as config_file:
        raw_config = yaml.safe_load(config_file) or {}

    camera_data: Dict[str, Any] = raw_config.get("camera", {})
    ui_data: Dict[str, Any] = raw_config.get("ui", {})
    calibration_data: Dict[str, Any] = raw_config.get("calibration", {})
    marker_data: Dict[str, Any] = raw_config.get("marker", {})
    drawing_data: Dict[str, Any] = raw_config.get("drawing", {})

    camera = CameraConfig(
        preview_size=_normalize_tuple(camera_data.get("preview_size", (640, 480)), 2),
        interleaved=bool(camera_data.get("interleaved", False)),
        stream_name=str(camera_data.get("stream_name", "rgb")),
        intrinsics=camera_data.get("intrinsics", [[500.38571167, 0.0, 314.06344604], [0.0, 500.47668457, 238.7240448], [0.0, 0.0, 1.0]]),
        distortion_coeffs=camera_data.get("distortion_coeffs", [-4.14610481e+00, 1.10561991e+01, -3.34565295e-04, -5.48989163e-04, -7.81179380e+00, -4.22761488e+00, 1.13181620e+01, -8.09042549e+00, 0.0, 0.0, 0.0, 0.0, -7.13373360e-04, -1.07512390e-03]),
    )

    ui = UIConfig(
        window_name=str(ui_data.get("window_name", "image")),
        points_required=int(ui_data.get("points_required", 4)),
    )

    world_points = calibration_data.get(
        "world_points",
        [
            [0.0, 0.0],
            [10.0, 0.0],
            [10.0, 10.0],
            [0.0, 10.0],
        ],
    )
    calibration = CalibrationConfig(
        world_points=_normalize_point_list(world_points),
        target_world_point=_normalize_tuple(
            calibration_data.get("target_world_point", (1.0, 1.0)), 2
        ),
    )

    marker = MarkerConfig(
        color=_normalize_tuple(marker_data.get("color", (0, 0, 255)), 3),
        radius=int(marker_data.get("radius", 5)),
        thickness=int(marker_data.get("thickness", -1)),
    )

    drawing = DrawingConfig(
        workspace_color=_normalize_tuple(drawing_data.get("workspace_color", (255, 0, 0)), 3),
        workspace_thickness=int(drawing_data.get("workspace_thickness", 2)),
    )

    return AppConfig(camera=camera, ui=ui, calibration=calibration, marker=marker, drawing=drawing)
