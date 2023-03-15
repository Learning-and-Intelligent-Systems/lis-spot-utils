from dataclasses import dataclass
import numpy as np
from typing import Optional
from bosdyn.client.math_helpers import SE3Pose


@dataclass
class Intrinsics():
    rows: int
    cols: int
    fx: float
    fy: float
    cx: float
    cy: float

@dataclass
class RGBDImage():
    rgb: np.ndarray[np.int8]
    frame: SE3Pose
    depth_scale: float = 1

@dataclass
class DepthImage():
    rgb: np.ndarray[np.int16]
    frame: SE3Pose
    depth_scale: float = 1

@dataclass
class RGBImage():
    rgb: np.ndarray[np.int8]
    depth: np.ndarray[np.int16]
    frame: SE3Pose

@dataclass
class PointCloud():
    points_xyz: np.ndarray[np.float64]
    points_rgb: Optional[np.ndarray[np.int8]]
