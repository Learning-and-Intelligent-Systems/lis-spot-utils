
from controllers.startup import setup_robot
from controllers.arm import scan_room
from perception.conversion import rgbds_to_pointcloud
import open3d as o3d

if __name__ == "__main__":
    """
        Scan the scene using only the gripper 
        camera and visualize the pointcloud in open3d
    """

    robot_client = setup_robot()
    rgbds = scan_room(robot_client, num_images=20)
    pointcloud = rgbds_to_pointcloud(rgbds)

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(pointcloud.points_xyz)
    point_cloud.colors = o3d.utility.Vector3dVector(pointcloud.points_rgb)

    o3d.visualization.draw_geometries([point_cloud])