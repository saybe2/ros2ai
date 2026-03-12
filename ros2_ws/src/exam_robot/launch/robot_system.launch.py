from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory("exam_robot"))
    urdf_path = package_share / "urdf" / "exam_robot.urdf"
    rviz_config_path = package_share / "rviz" / "exam_robot.rviz"
    robot_description = urdf_path.read_text(encoding="utf-8")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "discharge_rate",
                default_value="1.0",
                description="Battery discharge rate in percent per second.",
            ),
            DeclareLaunchArgument(
                "max_speed",
                default_value="0.3",
                description="Max linear speed for ALL OK mode in m/s.",
            ),
            DeclareLaunchArgument(
                "start_rviz",
                default_value="true",
                description="Start RViz with exam_robot config.",
            ),
            Node(
                package="exam_robot",
                executable="battery_node",
                name="battery_node",
                output="screen",
                parameters=[{"discharge_rate": LaunchConfiguration("discharge_rate")}],
            ),
            Node(
                package="exam_robot",
                executable="distance_sensor",
                name="distance_sensor",
                output="screen",
            ),
            Node(
                package="exam_robot",
                executable="robot_controller",
                name="robot_controller",
                output="screen",
                parameters=[{"max_speed": LaunchConfiguration("max_speed")}],
            ),
            Node(
                package="exam_robot",
                executable="status_display",
                name="status_display",
                output="screen",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                output="screen",
                parameters=[
                    {"robot_description": robot_description},
                    {"rate": 30.0},
                ],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", str(rviz_config_path)],
                condition=IfCondition(LaunchConfiguration("start_rviz")),
            ),
        ]
    )
