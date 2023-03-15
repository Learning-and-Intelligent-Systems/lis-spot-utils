
from bosdyn.client.robot_command import RobotCommandBuilder
from structures.robot import RobotClient


def open_gripper(robot_client:RobotClient):
    # Make the open gripper RobotCommand
    gripper_command = RobotCommandBuilder.\
        claw_gripper_open_fraction_command(1.0)

    # Send the request
    _ = robot_client.command_client.robot_command(gripper_command)
    robot_client.robot.logger.info('Moving arm to position.')