import bosdyn.client
import bosdyn.client.estop
import bosdyn.client.lease
import bosdyn.client.util
from bosdyn.client.image import ImageClient
from bosdyn.client.manipulation_api_client import ManipulationApiClient
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient

from spot_utils.structures.robot import RobotClient

LIS_SPOT_IP = "192.168.80.3"

def setup_robot(spot_ip:str = LIS_SPOT_IP) -> RobotClient:
    bosdyn.client.util.setup_logging(False)

    sdk = bosdyn.client.create_standard_sdk('RobotClient')
    robot = sdk.create_robot(spot_ip)

    bosdyn.client.util.authenticate(robot)
    robot.time_sync.wait_for_sync()

    lease_client = robot.ensure_client(
        bosdyn.client.lease.LeaseClient.default_service_name)
    state_client: RobotStateClient = robot.ensure_client(
        RobotStateClient.default_service_name)
    command_client: RobotCommandClient = \
        robot.ensure_client(RobotCommandClient.default_service_name)
    image_client = robot.ensure_client(
        ImageClient.default_service_name)
    manipulation_client = robot.ensure_client(
        ManipulationApiClient.default_service_name)
    lease_keepalive = bosdyn.client.lease.LeaseKeepAlive(
        lease_client, must_acquire=True, return_at_exit=True)

    return RobotClient(robot=robot,
                       sdk=sdk,
                       state_client=state_client,
                       command_client=command_client,
                       image_client=image_client,
                       manipulation_client=manipulation_client,
                       lease_keepalive=lease_keepalive)

