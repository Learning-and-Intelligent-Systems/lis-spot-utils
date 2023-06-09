"""Data structures for the robot and robot parts."""

from dataclasses import dataclass
from typing import List

from bosdyn.client.image import ImageClient
from bosdyn.client.lease import LeaseKeepAlive
from bosdyn.client.manipulation_api_client import ManipulationApiClient
from bosdyn.client.robot import Robot
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.sdk import Sdk


@dataclass
class RobotClient:
    """All robot clients packaged into one object."""

    robot: Robot
    sdk: Sdk
    state_client: RobotStateClient
    command_client: RobotCommandClient
    image_client: ImageClient
    manipulation_client: ManipulationApiClient
    lease_keepalive: LeaseKeepAlive


@dataclass
class ArmJointPositions:
    """Arm joint positions."""

    sh0: float = 0
    sh1: float = 0
    el0: float = 0
    el1: float = 0
    wr0: float = 0
    wr1: float = 0

    def to_list(self) -> List[float]:
        """Converts the arm joints to a list."""
        return [self.sh0, self.sh1, self.el0, self.el1, self.wr0, self.wr1]

    @staticmethod
    def from_list(pos: List[float]):
        """Converts a list of joint positions into a ArmJointPositions
        object."""
        return ArmJointPositions(*pos)
