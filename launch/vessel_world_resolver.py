"""Resolve a vessel/world/rendering launch choice to a simulator invocation.

Kept as a plain, dependency-free function so it can be unit tested without
going through the ROS 2 launch/graph machinery.
"""

import os


def resolve_simulation_launch(
    vessel,
    world,
    rendering,
    sim_share_dir,
    simulation_data,
    simulation_rate,
    window_res_x,
    window_res_y,
    rendering_quality,
):
    """Resolve launch arguments to a simulator executable and its inputs.

    Args:
        vessel: Vessel name, e.g. 'voyager' or 'blueboat'.
        world: World name, e.g. 'mclab'.
        rendering: True for the GPU-rendering simulator, False for headless.
        sim_share_dir: Installed share directory of this package.
        simulation_data: Path to the simulation data folder.
        simulation_rate: Physics update rate [Hz], as a string.
        window_res_x: Render window width, as a string.
        window_res_y: Render window height, as a string.
        rendering_quality: Rendering quality (low/medium/high).

    Returns:
        A dict with 'executable', 'arguments', 'world_file', 'vessel_file',
        and 'scenario_file'.
    """
    world_file = os.path.join(sim_share_dir, 'worlds', f'{world}.scn')
    vessel_file = os.path.join(sim_share_dir, 'vessel_models', f'{vessel}.scn')
    scenario_file = os.path.join(sim_share_dir, 'scenarios', 'simulation.scn')

    if rendering:
        executable = 'stonefish_simulator'
        arguments = [
            simulation_data, scenario_file, simulation_rate,
            window_res_x, window_res_y, rendering_quality,
        ]
    else:
        executable = 'stonefish_simulator_nogpu'
        arguments = [simulation_data, scenario_file, simulation_rate]

    return {
        'executable': executable,
        'arguments': arguments,
        'world_file': world_file,
        'vessel_file': vessel_file,
        'scenario_file': scenario_file,
    }
