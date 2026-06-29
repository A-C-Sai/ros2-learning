from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node

# import os
# from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    urdf_path = PathJoinSubstitution([
        FindPackageShare('my_robot_description'),
        'urdf',
        'my_robot.urdf'
    ])

    # urdf_path = os.path.join(get_package_share_directory('my_robot_description'),
    #                          'urdf', 'my_robot.urdf')

    rviz_config_path = PathJoinSubstitution([
        FindPackageShare('my_robot_description'),
        'rviz',
        'config_file.rviz'
    ])

    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path],
        prefix="vglrun"
    )

    rqt_graph_node = Node(
        package='rqt_graph',
        executable='rqt_graph'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node,
        rqt_graph_node
    ])
