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

    rgb: np.ndarray
    frame: SE3Pose
    intrinsics: Intrinsics


@dataclass
class DepthImage:
    """Depth image."""

    depth: np.ndarray
    frame: SE3Pose
    intrinsics: Intrinsics
    depth_scale: float = 1


@dataclass
class RGBDImage:
    """Color + depth image."""

    rgb: np.ndarray
    depth: np.ndarray
    frame: SE3Pose
    intrinsics: Intrinsics
    depth_scale: float = 1


@dataclass
class PointCloud:
    """Cloud of points with positions and colors."""

    xyz: np.ndarray
    rgb: Optional[np.ndarray]
