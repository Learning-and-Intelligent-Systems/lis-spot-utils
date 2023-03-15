"""Data structures for images and pointclouds."""

from dataclasses import dataclass
from typing import Optional

import numpy as np
from bosdyn.client.math_helpers import SE3Pose


@dataclass
class Intrinsics:
    """Camera intrinsics."""

    rows: int
    cols: int
    fx: float
    fy: float
    cx: float
    cy: float


@dataclass
class RGBImage:
    """Color image."""

    rgb: np.ndarray[np.int8]
    frame: SE3Pose


@dataclass
class DepthImage:
    """Depth image."""

    depth: np.ndarray[np.int16]
    frame: SE3Pose
    depth_scale: float = 1


@dataclass
class RGBDImage:
    """Color + depth image."""

    rgb: np.ndarray[np.int8]
    depth: np.ndarray[np.int16]
    depth_scale: float = 1
    frame: SE3Pose


@dataclass
class PointCloud:
    """Cloud of points with positions and colors."""

    points_xyz: np.ndarray[np.float64]
    points_rgb: Optional[np.ndarray[np.int8]]
