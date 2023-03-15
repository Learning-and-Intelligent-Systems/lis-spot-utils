"""Scan the scene using only the gripper camera and visualize the pointcloud in
open3d."""

import open3d as o3d

from spot_utils.controllers.arm import scan_room
from spot_utils.controllers.startup import setup_robot
from spot_utils.perception.conversion import rgbds_to_pointcloud
from spot_utils.perception.segmentation import scene_segment_image

if __name__ == "__main__":
    robot_client = setup_robot()
    rgbds = scan_room(robot_client, num_images=20)
    segmented_rgbs = [scene_segment_image(rgbd) for rgbd in rgbds]
    pointcloud = rgbds_to_pointcloud(segmented_rgbs)

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(pointcloud.points_xyz)
    point_cloud.colors = o3d.utility.Vector3dVector(pointcloud.points_rgb)

    o3d.visualization.draw_geometries([point_cloud])
