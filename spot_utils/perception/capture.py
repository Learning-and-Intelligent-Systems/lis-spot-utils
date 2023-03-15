
import cv2
from bosdyn.api import image_pb2
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, get_a_tform_b
from bosdyn.client.image import build_image_request
from numpy import np

from spot_utils.structures.image import DepthImage, RGBDImage, RGBImage
from spot_utils.structures.robot import RobotClient

CAMERAS = ["frontleft", "frontright", "left", "right", "back", "hand"]

SOURCES_DEPTH_FRAME = {cam: (cam + '_depth', cam + '_visual_in_depth_frame') for cam in CAMERAS[:-1]}
SOURCES_DEPTH_FRAME["hand"] = ("hand_depth", "hand_color_in_hand_depth_frame")

SOURCES_RGB_FRAME = {cam: (cam + '_depth_in_visual_frame', cam + '_fisheye_image') for cam in CAMERAS[:-1]}
SOURCES_RGB_FRAME["hand"] = ("hand_depth_in_hand_color_frame", "hand_color_image")

def capture_rgb(robot_client:RobotClient, source:str):
    reqs = [build_image_request(source, pixel_format=image_pb2.Image.PIXEL_FORMAT_RGB_U8)]
    image_responses = robot_client.image_client.get_image(reqs)
    
    t = get_a_tform_b(image_responses[0].shot.transforms_snapshot, \
        BODY_FRAME_NAME, image_responses[0].shot.frame_name_image_sensor)
    
    cv_visual = cv2.imdecode(np.frombuffer(image_responses[0].shot.image.data, dtype=np.uint8), -1)
    cv_visual = cv2.cvtColor(cv_visual, cv2.COLOR_BGR2RGB)

    return RGBImage(rgb=cv_visual, frame=t)

def capture_depth(robot_client:RobotClient, source:str):
    reqs = [build_image_request(source, pixel_format=image_pb2.Image.PIXEL_FORMAT_DEPTH_U16)]
    image_responses = robot_client.image_client.get_image(reqs)
        
    t = get_a_tform_b(image_responses[0].shot.transforms_snapshot, \
        BODY_FRAME_NAME, image_responses[0].shot.frame_name_image_sensor)
    
    cv_dep = cv2.imdecode(np.frombuffer(image_responses[0].shot.image.data, dtype=np.uint16), -1)

    return RGBImage(rgb=cv_dep, frame=t)

def capture_rgbd(robot_client:RobotClient, camera:str, in_frame:str="depth") -> RGBDImage:
    rgb_source = SOURCES_DEPTH_FRAME[camera] if in_frame == "depth" \
                    else SOURCES_RGB_FRAME[camera]
    depth_source = SOURCES_DEPTH_FRAME[camera] if in_frame == "depth" \
                    else SOURCES_RGB_FRAME[camera]
    
    rgb = capture_rgb(robot_client, rgb_source)    
    depth = capture_depth(robot_client, depth_source)
    
    rgbd = RGBDImage(rgb.rgb, depth.depth, depth.frame) if in_frame == "depth" \
            else RGBDImage(rgb.rgb, depth.depth, rgb.frame)

    return rgbd
