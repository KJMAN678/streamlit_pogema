import base64

import numpy as np
import streamlit as st

from pogema import GridConfig, pogema_v0
from pogema.animation import AnimationMonitor


def render_svg(svg_file_path):
    """Renders the given svg string."""
    f = open(svg_file_path, "r")
    lines = f.readlines()
    line_string = "".join(lines)

    b64 = base64.b64encode(line_string.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


def mapf(file_path, num_agents):
    grid = """
    .....#.....
    .....#.....
    ...........
    .....#.....
    .....#.....
    #.####.....
    .....###.##
    .....#.....
    .....#.....
    ...........
    .....#.....
    """

    agents_xy = np.random.randint(2, 4, (num_agents, 2)).tolist()
    targets_xy = np.random.randint(2, 4, (num_agents, 2)).tolist()

    grid_config = GridConfig(
        num_agents=num_agents,
        density=0.4,
        seed=1,
        max_episode_steps=128,
        obs_radius=3,
        map=grid,
        agents_xy=agents_xy,
        targets_xy=targets_xy,
    )

    env = pogema_v0(grid_config=grid_config)
    env = AnimationMonitor(env)

    obs, info = env.reset()

    terminated = truncated = [False, ...]

    while not all(terminated) and not all(truncated):
        # Use random policy to make actions
        obs, reward, terminated, truncated, info = env.step(
            [env.action_space.sample() for _ in range(grid_config.num_agents)]
        )

    env.save_animation(file_path)


def main():
    file_path = "videos/mapf.svg"

    num_agents = int(st.slider("エージェントの数", 1, 30, 1))

    if st.button("実行"):
        mapf(file_path, num_agents)
        render_svg(file_path)


if __name__ == "__main__":
    main()
