from dataclasses import dataclass
from bosdyn.client.sdk import Sdk
from bosdyn.client.robot import Robot
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.image import ImageClient
from bosdyn.client.manipulation_api_client import ManipulationApiClient
from bosdyn.client.lease import LeaseKeepAlive

@dataclass
class RobotClient:
    robot: Robot
    sdk: Sdk
    state_client: RobotStateClient
    command_client: RobotCommandClient
    image_client: ImageClient
    manipulation_client: ManipulationApiClient
    lease_keepalive: LeaseKeepAlive