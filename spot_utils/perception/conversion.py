
from bosdyn.client.image import _depth_image_get_valid_indices, \
    _depth_image_data_to_numpy
import numpy as np
from typing import List

from structures.image import RGBDImage, PointCloud

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
    xyz = np.vstack((x, y, z)).T

    return PointCloud(xyz=rgbd.frame.transform_cloud(np.array(xyz)), rgb=rgb) 

def rgbds_to_pointcloud(rgbds:List[RGBDImage]) -> PointCloud:
    local_pointclouds = [rgbd_to_pointcloud(rgbd) for rgbd in rgbds]
    return PointCloud(xyz=np.concatenate([p.xyz for p in local_pointclouds], axis=0),
                      rgb=np.concatenate([p.rgb for p in local_pointclouds], axis=0))
