# from launch import LaunchDescription
# from launch_ros.actions import Node
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare

# # from ament_index_python.packages import get_package_share_directory
# # import os


# def generate_launch_descriptio():

#     # create a dynamic obj that will have a value at runtime
#     config_file = LaunchConfiguration('config_file')

#     # declare a launch argument for the YA config file name
#     config_file_arg = DeclareLaunchArgument(
#         'config_file',
#         default_value='template_config.yaml',
#         description="Path to the YAML config file"
#     )

#     # build the full path to the config file at runtime
#     config_path = PathJoinSubstitution([
#         FindPackageShare('bringup'),
#         'config',
#         config_file,
#     ])

#     # OR

#     # param_config = os.path.join(get_package_share_directory("bringup"),
#     #                             "config", "<filename>.yaml")

#     # create a launch file description
#     ld = LaunchDescription()
#     nodes = []

#     # ___ node
#     nodes.append(Node(
#         package="",
#         executable="",
#         namespace="",
#         name="",
#         parameters=[{
#             'param': value,
#             'param': "value",
#         }]
#     ))

#     # ___ node
#     nodes.append(Node(
#         package="",
#         executable="",
#         namespace="",
#         name="",
#         parameters=[config_path]
#     ))

#     # ___ node
#     # nodes.append(Node(
#     #     package="",
#     #     executable="",
#     #     namespace="",
#     #     name="",
#     #     parameters=[param_config]
#     # ))

#     # ___ node
#     nodes.append(Node(
#         package="",
#         executable="",
#         name="",
#         remappings=[
#             # having a leading slash is like have a exact match, may break with change
#             # of namespaces.
#             ("/old_topic/service/action", "/new_topic/service/action"),
#         ]
#     ))

#     # add argument(s) to launch description
#     ld.add_action(config_file_arg)

#     # add nodes to launch description
#     for node in nodes:
#         ld.add_action(node)

#     return ld
