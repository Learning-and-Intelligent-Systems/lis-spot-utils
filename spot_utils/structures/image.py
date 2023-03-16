"""Data structures for images and pointclouds."""

from dataclasses import dataclass

import numpy as np
from bosdyn.client.math_helpers import SE3Pose
from numpy.typing import NDArray


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

    rgb: NDArray[np.uint8]
    frame: SE3Pose
    intrinsics: Intrinsics


@dataclass
class DepthImage:
    """Depth image."""

    depth: NDArray[np.uint16]
    frame: SE3Pose
    intrinsics: Intrinsics
    depth_scale: float = 1


@dataclass
class RGBDImage:
    """Color + depth image."""

    rgb: NDArray[np.uint8]
    depth: NDArray[np.uint16]
    frame: SE3Pose
    intrinsics: Intrinsics
    depth_scale: float = 1


@dataclass
class PointCloud:
    """Cloud of points with positions and colors."""

    xyz: NDArray[np.float64]
    rgb: NDArray[np.uint8]
