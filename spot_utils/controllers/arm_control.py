"""Functions for controlling the arm on spot."""

import time
from logging import Logger
from typing import Any, List

import numpy as np
from bosdyn.api import arm_command_pb2, robot_command_pb2, synchronized_command_pb2
from bosdyn.client.robot_command import RobotCommandBuilder
from bosdyn.util import duration_to_seconds

from spot_utils.perception.capture import capture_rgbd
from spot_utils.structures.image import RGBDImage
from spot_utils.structures.robot import ArmJointPositions, RobotClient


def open_gripper(robot_client: RobotClient):
    """Helper function to open the robot gripper."""
    # Make the open gripper RobotCommand
    gripper_command = RobotCommandBuilder.claw_gripper_open_fraction_command(1.0)

    # Send the request
    _ = robot_client.command_client.robot_command(gripper_command)
    robot_client.robot.logger.info("Moving arm to position.")


def _print_feedback(feedback_resp: Any, logger: Logger) -> float:
    """Helper function to query for ArmJointMove feedback, and print it to the
    console.

    Returns the time_to_goal value reported in the feedback

    feedback_resp is a protobuf with type Any
    """
    sync_feedback = feedback_resp.feedback.synchronized_feedback
    arm_feedback = sync_feedback.arm_command_feedback
    joint_move_feedback = arm_feedback.arm_joint_move_feedback

    logger.info(f"  planner_status = {joint_move_feedback.planner_status}")
    logger.info(
        f"  time_to_goal = \
            {duration_to_seconds(joint_move_feedback.time_to_goal):.2f} seconds."
    )

    # Query planned_points to determine target pose of arm
    logger.info("  planned_points:")
    for idx, points in enumerate(joint_move_feedback.planned_points):
        pos = points.position
        pos_str = f"sh0 = {pos.sh0.value:.3f}, \
                    sh1 = {pos.sh1.value:.3f}, \
                    el0 = {pos.el0.value:.3f}, \
                    el1 = {pos.el1.value:.3f}, \
                    wr0 = {pos.wr0.value:.3f}, \
                    wr1 = {pos.wr1.value:.3f}"
        logger.info(f"    {idx}: {pos_str}")
    return duration_to_seconds(joint_move_feedback.time_to_goal)


def move_arm(robot_client: RobotClient, arm_pos: ArmJointPositions):
    """Helper function to move the robot joints to target joint positions."""
    traj_point = RobotCommandBuilder.create_arm_joint_trajectory_point(
        *arm_pos.to_list()
    )

    arm_joint_traj = arm_command_pb2.ArmJointTrajectory(points=[traj_point])
    # Make a RobotCommand

    joint_move_command = arm_command_pb2.ArmJointMoveCommand.Request(
        trajectory=arm_joint_traj
    )
    arm_command = arm_command_pb2.ArmCommand.Request(
        arm_joint_move_command=joint_move_command
    )
    sync_arm = synchronized_command_pb2.SynchronizedCommand.Request(
        arm_command=arm_command
    )
    arm_sync_robot_cmd = robot_command_pb2.RobotCommand(synchronized_command=sync_arm)
    command = RobotCommandBuilder.build_synchro_command(arm_sync_robot_cmd)

    # Send the request
    cmd_id = robot_client.command_client.robot_command(command)
    robot_client.robot.logger.info("Moving arm to position 1.")

    # Query for feedback to determine how long the goto will take.
    feedback_resp = robot_client.command_client.robot_command_feedback(cmd_id)
    robot_client.robot.logger.info("Feedback for Example 1: single point goto")
    time_to_goal = _print_feedback(feedback_resp, robot_client.robot.logger)
    time.sleep(time_to_goal)


def scan_room(robot_client: RobotClient, num_images: int = 20) -> List[RGBDImage]:
    """Helper function to scan the room using a sequence of RGBD images from
    several arm joint positions that form a circular 360 degree gripper
    path."""
    pos = ArmJointPositions.from_list([0, -2.0, 1.0, 0.0, 1.6, 0.0])
    rgbds = []
    for t in range(num_images):
        edge = np.pi / 8.0
        pos.sh0 = (np.pi * 2 - 2 * edge) * float(t) / float(num_images) - np.pi + edge
        move_arm(robot_client, arm_pos=pos)
        rgbds.append(capture_rgbd(robot_client, camera="hand"))
    return rgbds
