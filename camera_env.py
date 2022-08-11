import metaworld
import random
import numpy as np
import os
import imageio
from envs.sawyer_drawer_open_v2_change_camera import SawyerDrawerOpenEnvV2_ChangeCamera

def save_gif(episode_name, episode_obs, dur=0.01, dir='gif'):
    os.makedirs(dir, exist_ok=True)
    with imageio.get_writer(os.path.join(dir,episode_name), mode='I', duration=dur) as writer:
        for obs_np in episode_obs:
            writer.append_data(obs_np)

env_name = 'drawer-open-left-camera'
camera_name = 'left'
env = SawyerDrawerOpenEnvV2_ChangeCamera()


episode_return = 0
episode_len = 0
episode_done = 0
episode_obs = []

dur = 0.01
width = 250
height = 200

obs = env.reset()  # Reset environment
for i in range(0,1):
    for j in range(0, 200):
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
    env.reset()
    print(f'Episode {i}_{episode_done}, cum. return: {episode_return:0.1f}, length: {episode_len}.')
    episode_name = f'ep_{i}_{env_name}_camera_{camera_name}.gif'
    save_gif(episode_name, episode_obs, dur)
    episode_return = 0
    episode_len = 0
    episode_obs = []
    
