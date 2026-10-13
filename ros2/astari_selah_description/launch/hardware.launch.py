from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('astari_selah_description')
    serial_port = LaunchConfiguration('serial_port')

    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_share, 'launch', 'display.launch.py'])
        ),
        launch_arguments={
            'use_gui': 'false',
            'use_esp32': 'true',
            'serial_port': serial_port
        }.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'serial_port',
            default_value='/dev/ttyUSB0',
            description='Serial port path for the ESP32 microcontroller'
        ),
        display_launch
    ])
