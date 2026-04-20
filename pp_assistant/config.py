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
class DatasetConfig:
    base_path: str = "data/datasets"

@dataclass
class ObjectConfig:
    id: int
    label: str
    width: float
    height: float
    color: Tuple[int, int, int]

@dataclass
class ObjectsConfig:
    objects: List[ObjectConfig] = field(default_factory=list)


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
class CellLabelConfig:
    font_scale: float = 0.5
    font_thickness: int = 1
    bg_padding: int = 5
    show_label: bool = True


@dataclass
class DrawingConfig:
    workspace_color: Tuple[int, int, int] = (255, 0, 0)
    workspace_thickness: int = 2
    cell_label: CellLabelConfig = field(default_factory=CellLabelConfig)


@dataclass
class AppConfig:
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    objects: ObjectsConfig = field(default_factory=ObjectsConfig)
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

    dataset_data: Dict[str, Any] = raw_config.get("datasets", {})
    camera_data: Dict[str, Any] = raw_config.get("camera", {})
    ui_data: Dict[str, Any] = raw_config.get("ui", {})
    calibration_data: Dict[str, Any] = raw_config.get("calibration", {})
    marker_data: Dict[str, Any] = raw_config.get("marker", {})
    drawing_data: Dict[str, Any] = raw_config.get("drawing", {})

    dataset = DatasetConfig(
        base_path=str(dataset_data.get("base_path", "/pp_assistant/datasets"))
    )

    objects_data: List[Dict[str, Any]] = raw_config.get("objects", [])
    objects_list = [
        ObjectConfig(
            id=int(obj.get("id", 0)),
            label=str(obj.get("label", "")),
            width=float(obj.get("width", 0.0)),
            height=float(obj.get("height", 0.0)),
            color=_normalize_tuple(obj.get("color", (0, 0, 0)), 3),
        )
        for obj in objects_data
    ]
    objects = ObjectsConfig(objects=objects_list)

    camera = CameraConfig(
        preview_size=_normalize_tuple(camera_data.get("preview_size", (640, 480)), 2),
        interleaved=bool(camera_data.get("interleaved", False)),
        stream_name=str(camera_data.get("stream_name", "rgb")),
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

    cell_label_data: Dict[str, Any] = drawing_data.get("cell_label", {})
    cell_label = CellLabelConfig(
        font_scale=float(cell_label_data.get("font_scale", 0.5)),
        font_thickness=int(cell_label_data.get("font_thickness", 1)),
        bg_padding=int(cell_label_data.get("bg_padding", 5)),
        show_label=bool(cell_label_data.get("show_label", True)),
    )

    drawing = DrawingConfig(
        workspace_color=_normalize_tuple(drawing_data.get("workspace_color", (255, 0, 0)), 3),
        workspace_thickness=int(drawing_data.get("workspace_thickness", 2)),
        cell_label=cell_label,
    )

    return AppConfig(dataset=dataset, camera=camera, ui=ui, calibration=calibration, marker=marker, drawing=drawing, objects=objects)
