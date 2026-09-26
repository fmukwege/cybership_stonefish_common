import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

# vessel_world_resolver.py lives alongside this file; ros2 launch loads this
# module via SourceFileLoader without adding its directory to sys.path, so
# make the sibling module importable explicitly.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vessel_world_resolver import resolve_simulation_launch  # noqa: E402


def launch_setup(context: LaunchContext, *args, **kwargs):
    sim_dir = get_package_share_directory('cybership_simulation_common')

    resolved = resolve_simulation_launch(
        vessel=LaunchConfiguration('vessel').perform(context),
        world=LaunchConfiguration('world').perform(context),
        rendering=LaunchConfiguration('rendering').perform(context).lower() == 'true',
        sim_share_dir=sim_dir,
        simulation_data=LaunchConfiguration('simulation_data').perform(context),
        simulation_rate=LaunchConfiguration('simulation_rate').perform(context),
        window_res_x=LaunchConfiguration('window_res_x').perform(context),
        window_res_y=LaunchConfiguration('window_res_y').perform(context),
        rendering_quality=LaunchConfiguration('rendering_quality').perform(context),
    )

    sim_node = Node(
        package='stonefish_ros2',
        executable=resolved['executable'],
        namespace='stonefish_ros2',
        name=resolved['executable'],
        arguments=resolved['arguments'],
        parameters=[{
            'world_file': resolved['world_file'],
            'vessel_file': resolved['vessel_file'],
        }],
        output='screen',
    )

    return [sim_node]


def generate_launch_description():
    sim_dir = get_package_share_directory('cybership_simulation_common')

    return LaunchDescription([
        DeclareLaunchArgument(
            'vessel',
            default_value='voyager',
            description='Vessel to load',
            choices=['voyager', 'blueboat']
        ),
        DeclareLaunchArgument(
            'world',
            default_value='mclab',
            description='World (environment) to load',
            choices=['mclab']
        ),
        DeclareLaunchArgument(
            'rendering',
            default_value='true',
            description='Enable GPU rendering (true/false); false runs the headless simulator'
        ),
        DeclareLaunchArgument(
            'simulation_data',
            default_value=PathJoinSubstitution([sim_dir, 'data']),
            description='Path to the simulation data folder'
        ),
        DeclareLaunchArgument(
            'simulation_rate',
            default_value='100.0',
            description='Physics update rate [Hz]'
        ),
        DeclareLaunchArgument(
            'window_res_x',
            default_value='2460',
            description='Window resolution width'
        ),
        DeclareLaunchArgument(
            'window_res_y',
            default_value='1340',
            description='Window resolution height'
        ),
        DeclareLaunchArgument(
            'rendering_quality',
            default_value='high',
            description='Rendering quality (low/medium/high)'
        ),
        OpaqueFunction(function=launch_setup),
    ])
