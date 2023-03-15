"""Scan the scene using only the gripper camera, segment the scene with an
image scene segmentation network, project the segmentations into a 3d
pointcloud, and visualize the segmented pointcloud."""

import open3d as o3d

from spot_utils.controllers.arm import scan_room
from spot_utils.controllers.startup import setup_robot
from spot_utils.perception.conversion import rgbds_to_pointcloud

if __name__ == "__main__":
    robot_client = setup_robot()
    rgbds = scan_room(robot_client, num_images=20)

    pointcloud = rgbds_to_pointcloud(rgbds)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(pointcloud.points_xyz)
    point_cloud.colors = o3d.utility.Vector3dVector(pointcloud.points_rgb)

    o3d.visualization.draw_geometries([point_cloud])
