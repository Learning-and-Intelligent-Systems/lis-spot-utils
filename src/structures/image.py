from dataclasses import dataclass
import numpy as np
from typing import Optional
from bosdyn.client.math_helpers import SE3Pose
from bosdyn.client.image import _depth_image_get_valid_indices, \
    _depth_image_data_to_numpy

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

def rgbd_to_pointcloud(rgbd:RGBDImage, min_dist:int=0, max_dist:int=1000) -> PointCloud:

    # Convert the proto representation into a numpy array.
    depth_array = _depth_image_data_to_numpy(rgbd.depth)

    # Determine which indices have valid data in the user requested range.
    valid_inds = _depth_image_get_valid_indices(depth_array, 
                                                np.rint(min_dist * rgbd.depth_scale),
                                                np.rint(max_dist * rgbd.depth_scale))

    # Compute the valid data.
    rows, cols = np.mgrid[0:rgbd.intrinsics.rows, 0:rgbd.intrinsics.cols]
    depth_array = depth_array[valid_inds]
    rows = rows[valid_inds]
    cols = cols[valid_inds]

    # Convert the valid distance data to (x,y,z) values expressed in the sensor frame.
    z = depth_array / rgbd.depth_scale
    x = np.multiply(z, (cols - rgbd.intrinsics.cx)) / rgbd.intrinsics.fx
    y = np.multiply(z, (rows - rgbd.intrinsics.cy)) / rgbd.intrinsics.fy

    cv_visual = rgbd.rgb
    # cv_visual = cv2.cvtColor(cv_visual, cv2.COLOR_BGR2RGB)
    rgb = np.array(cv_visual[rows, cols])

    return PointCloud(xyz=np.vstack((x, y, z)).T, rgb=rgb) 
