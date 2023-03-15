from dataclasses import dataclass
from bosdyn.client.sdk import Sdk
from bosdyn.client.robot import Robot
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.image import ImageClient
from bosdyn.client.manipulation_api_client import ManipulationApiClient
from bosdyn.client.lease import LeaseKeepAlive
from typing import List


@dataclass
class RobotClient:
    robot: Robot
    sdk: Sdk
    state_client: RobotStateClient
    command_client: RobotCommandClient
    image_client: ImageClient
    manipulation_client: ManipulationApiClient
    lease_keepalive: LeaseKeepAlive

@dataclass
class ArmJointPositions:
    sh0:float = 0
    sh1:float = 0
    el0:float = 0
    el1:float = 0
    wr0:float = 0
    wr1:float = 0

    def to_list(self):
        return [self.sh0, self.sh1, self.el0, self.el1, self.wr0, self.wr1]

    @staticmethod
    def from_list(pos:List[float]):
        return ArmJointPositions(*pos)