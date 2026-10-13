import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('astari_selah_description')

    # Launch configuration variables
    use_gui = LaunchConfiguration('use_gui')
    use_esp32 = LaunchConfiguration('use_esp32')
    serial_port = LaunchConfiguration('serial_port')
    rviz_config = LaunchConfiguration('rviz_config')

    default_rviz_path = PathJoinSubstitution([pkg_share, 'rviz', 'display.rviz'])
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'astari_selah.urdf.xacro'])

    # Robot State Publisher node
    robot_description = Command([
        FindExecutable(name='xacro'), ' ', xacro_file
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': False
        }]
    )

    # Joint State Publisher GUI (Active when use_gui is true and use_esp32 is false)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(use_gui)
    )

    # Hardware ESP32 Bridge Node (Active when use_esp32 is true)
    esp32_bridge_node = Node(
        package='astari_selah_description',
        executable='esp32_bridge.py',
        output='screen',
        parameters=[{
            'port': serial_port,
            'baud': 115200,
            'simulation_fallback': True
        }],
        condition=IfCondition(use_esp32)
    )

    # RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_gui',
            default_value='true',
            description='Launch interactive joint_state_publisher_gui'
        ),
        DeclareLaunchArgument(
            'use_esp32',
            default_value='false',
            description='Launch live hardware ESP32 serial bridge'
        ),
        DeclareLaunchArgument(
            'serial_port',
            default_value='/dev/ttyUSB0',
            description='Serial port for ESP32 hardware bridge'
        ),
        DeclareLaunchArgument(
            'rviz_config',
            default_value=default_rviz_path,
            description='Absolute path to RViz layout file'
        ),
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        esp32_bridge_node,
        rviz_node
    ])
