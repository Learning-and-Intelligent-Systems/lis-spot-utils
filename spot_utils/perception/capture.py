"""Functions for collecting images from different cameras and camera sources on
the spot."""

from typing import Any

import cv2
import numpy as np
from bosdyn.api.image_pb2 import Image
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, get_a_tform_b
from bosdyn.client.image import _depth_image_data_to_numpy, build_image_request

from spot_utils.structures.image import DepthImage, Intrinsics, RGBDImage, RGBImage
from spot_utils.structures.robot import RobotClient

CAMERAS = ["frontleft", "frontright", "left", "right", "back", "hand"]

SOURCES_DEPTH_FRAME = {
    cam: (cam + "_depth", cam + "_visual_in_depth_frame") for cam in CAMERAS[:-1]
}
SOURCES_DEPTH_FRAME["hand"] = ("hand_depth", "hand_color_in_hand_depth_frame")

SOURCES_RGB_FRAME = {
    cam: (cam + "_depth_in_visual_frame", cam + "_fisheye_image")
    for cam in CAMERAS[:-1]
}
SOURCES_RGB_FRAME["hand"] = ("hand_depth_in_hand_color_frame", "hand_color_image")


def get_intrinsics(response: Any) -> Intrinsics:
    """Get the camera intrinsics from an image response.

    response is a protobuf given type Any
    """
    intrinsics = response.source.pinhole.intrinsics
    return Intrinsics(
        response.source.rows,
        response.source.cols,
        intrinsics.focal_length.x,
        intrinsics.focal_length.y,
        intrinsics.principal_point.x,
        intrinsics.principal_point.y,
    )


def capture_rgb(robot_client: RobotClient, source: str):
    """Capture just the rgb image with a particular camera source."""

    f = Image.PIXEL_FORMAT_RGB_U8  # pylint:disable=no-member
    reqs = [build_image_request(source, pixel_format=f)]
    image_responses = robot_client.image_client.get_image(reqs)

    t = get_a_tform_b(
        image_responses[0].shot.transforms_snapshot,
        BODY_FRAME_NAME,
        image_responses[0].shot.frame_name_image_sensor,
    )

    data = image_responses[0].shot.image.data
    cv_visual = cv2.imdecode(
        np.frombuffer(data, dtype=np.uint8),  # type: ignore
        -1,
    )
    cv_visual = cv2.cvtColor(cv_visual, cv2.COLOR_BGR2RGB)

    return RGBImage(cv_visual, t, get_intrinsics(image_responses[0]))


def capture_depth(robot_client: RobotClient, source: str):
    """Capture just the depth image with a particular camera source."""

    f = Image.PIXEL_FORMAT_DEPTH_U16  # pylint:disable=no-member
    reqs = [build_image_request(source, pixel_format=f)]

    image_responses = robot_client.image_client.get_image(reqs)
    t = get_a_tform_b(
        image_responses[0].shot.transforms_snapshot,
        BODY_FRAME_NAME,
        image_responses[0].shot.frame_name_image_sensor,
    )

    cv_dep = _depth_image_data_to_numpy(image_responses[0])

    return DepthImage(
        cv_dep,
        t,
        get_intrinsics(image_responses[0]),
        image_responses[0].source.depth_scale,
    )


def capture_rgbd(
    robot_client: RobotClient, camera: str, in_frame: str = "rgb"
) -> RGBDImage:
    """Given a camera, capture the RGB/Depth and merge them into and RGBD data
    that is either in the depth frame or image frame depending on the value of
    in_frame."""
    depth_source, rgb_source = (
        SOURCES_DEPTH_FRAME[camera]
        if in_frame == "depth"
        else SOURCES_RGB_FRAME[camera]
    )

    rgb = capture_rgb(robot_client, rgb_source)
    depth = capture_depth(robot_client, depth_source)

    rgbd = (
        RGBDImage(
            rgb.rgb, depth.depth, depth.frame, depth.intrinsics, depth.depth_scale
        )
        if in_frame == "depth"
        else RGBDImage(
            rgb.rgb, depth.depth, rgb.frame, rgb.intrinsics, depth.depth_scale
        )
    )

    return rgbd
