"""Functions for converting between data types."""

from typing import List

import numpy as np
from bosdyn.client.image import _depth_image_get_valid_indices

from spot_utils.structures.image import PointCloud, RGBDImage


def rgbd_to_pointcloud(
    rgbd: RGBDImage, min_dist: int = 0, max_dist: int = 1000
) -> PointCloud:
    """Converts a single rgbd image to a pointcloud."""

    depth_array = rgbd.depth

    # Determine which indices have valid data in the user requested range.
    valid_inds = _depth_image_get_valid_indices(
        depth_array,
        np.rint(min_dist * rgbd.depth_scale),
        np.rint(max_dist * rgbd.depth_scale),
    )

    # Compute the valid data.
    rows, cols = np.mgrid[0 : rgbd.intrinsics.rows, 0 : rgbd.intrinsics.cols]
    depth_array = depth_array[valid_inds]
    rows = rows[valid_inds]
    cols = cols[valid_inds]

    # Convert the valid distance data to (x,y,z) values expressed in the sensor frame.
    z = depth_array / rgbd.depth_scale
    x = np.multiply(z, (cols - rgbd.intrinsics.cx)) / rgbd.intrinsics.fx
    y = np.multiply(z, (rows - rgbd.intrinsics.cy)) / rgbd.intrinsics.fy

    rgb = np.array(rgbd.rgb[rows, cols])
    xyz = np.vstack((x, y, z)).T

    return PointCloud(rgbd.frame.transform_cloud(np.array(xyz)), rgb)


def rgbds_to_pointcloud(rgbds: List[RGBDImage]) -> PointCloud:
    """Converts a set of rgbd images to a global pointcloud."""
    local_pointclouds = [rgbd_to_pointcloud(rgbd) for rgbd in rgbds]
    return PointCloud(
        np.concatenate([p.xyz for p in local_pointclouds], axis=0),  # type: ignore
        np.concatenate([p.rgb for p in local_pointclouds], axis=0),  # type: ignore
    )
