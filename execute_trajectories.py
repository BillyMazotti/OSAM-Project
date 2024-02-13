#!/usr/bin/python3

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs
import moveit_msgs
import geometry_msgs
import numpy as np
from scipy.spatial.transform import Rotation as R

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("panda_arm")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)


def plan_joint_goal():
    group_variable_values = group.get_current_joint_values()

    group_variable_values[0] = 0.723
    group_variable_values[1] = -0.521
    group_variable_values[2] = -0.220
    group_variable_values[3] = -2.165
    group_variable_values[4] = -0.109
    group_variable_values[5] = 1.653
    group_variable_values[6] = -0.720
    group.set_joint_value_target(group_variable_values)
    group.go(wait=True)


def plan_pose_goal(XYZ):
    pose_goal = geometry_msgs.msg.Pose()

    r = R.from_euler('zyx',[np.pi/4,np.pi/2,0],degrees=False)
    XYZW = r.as_quat()
    pose_goal.orientation.w = XYZW[3]
    pose_goal.orientation.x = XYZW[0]
    pose_goal.orientation.y = XYZW[1]
    pose_goal.orientation.z = XYZW[2]
    pose_goal.position.x = XYZ[0]
    pose_goal.position.y = XYZ[1]
    pose_goal.position.z = XYZ[2]
    group.set_pose_target(pose_goal)
    group.set_max_acceleration_scaling_factor(1.0)
    group.set_planning_time(2.0)
    group.set_max_velocity_scaling_factor(1.0)
    group.go(wait=True)


XYZ1 = [0.4,0.1,0.4]    # home position
XYZ2 = [0.5,0.1,0.4]    # move in +x
XYZ3 = [0.5,0.3,0.4]    # move in +y
XYZ4 = [0.5,0.3,0.8]    # move in +z

poses = [
    XYZ1,
    XYZ2,
    XYZ3,
    XYZ4,
    XYZ1
]
for pose in poses:

    plan_pose_goal(pose)


moveit_commander.roscpp_shutdown()

