import metaworld
import random
import numpy as np
import os
import imageio
from metaworld.envs import ALL_V2_ENVIRONMENTS_GOAL_OBSERVABLE

def save_gif(episode_name, episode_obs, dur=0.01, dir='gif'):
    os.makedirs(dir, exist_ok=True)
    with imageio.get_writer(os.path.join(dir,episode_name), mode='I', duration=dur) as writer:
        for obs_np in episode_obs:
            writer.append_data(obs_np)

print(metaworld.ML1.ENV_NAMES)  # Check out the available environments

env_name = 'drawer-open-v2-goal-observable'
camera_name = 'topview'
# ml1 = metaworld.ML1(env_name) # Construct the benchmark, sampling tasks

# env = ml1.train_classes[env_name]()  # Create an environment with task `pick_place`
# task = random.choice(ml1.train_tasks)
# env.set_task(task)  # Set task
breakpoint()
env  = ALL_V2_ENVIRONMENTS_GOAL_OBSERVABLE[env_name]()


episode_return = 0
episode_len = 0
episode_done = 0
episode_obs = []

dur = 0.01
width = 250
height = 200

obs = env.reset()  # Reset environment
for i in range(0,2):
    for j in range(0, 500):
        # breakpoint()
        # env.viewer.cam.lookat[0] = 0.1
        img = env.render(offscreen=True, camera_name=camera_name)
        # env.render()
        episode_obs.append(img)
        a = env.action_space.sample()  # Sample an action
        obs, reward, done, info = env.step(a)  # Step the environoment with the sampled random action
        episode_return += reward
        episode_len += 1
        if done:
            episode_done += 1
            break
    print(f'Episode {i}_{episode_done}, cum. return: {episode_return:0.1f}, length: {episode_len}.')
    episode_name = f'ep_{i}_{env_name}_camera_{camera_name}.gif'
    save_gif(episode_name, episode_obs, dur)
    episode_return = 0
    episode_len = 0
    episode_obs = []
    env.reset()