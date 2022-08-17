import metaworld
import random
import numpy as np
import os
import imageio
from envs.sawyer_drawer_open_v2_change_camera import SawyerDrawerOpenEnvV2_ChangeCamera
from envs.sawyer_push_v2 import SawyerPushEnv_ChangeV2

from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder
import wandb
from wandb.integration.sb3 import WandbCallback

from stable_baselines3 import SAC, PPO
from metaworld.envs import ALL_V2_ENVIRONMENTS_GOAL_OBSERVABLE

def save_gif(episode_name, episode_obs, dur=0.01, dir='gif'):
    os.makedirs(dir, exist_ok=True)
    with imageio.get_writer(os.path.join(dir,episode_name), mode='I', duration=dur) as writer:
        for obs_np in episode_obs:
            writer.append_data(obs_np)


config = {
    "policy_type": "MlpPolicy",
    "total_timesteps": 200000,
}

env_name = 'push-v2-goal-observable'
camera_name = 'topview'
env = SawyerPushEnv_ChangeV2()
model = SAC(config["policy_type"], env)


model.learn(
    total_timesteps=config["total_timesteps"]
)
model.save("sac_push")

env_name = 'push'
camera_name = 'topview'


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
        a, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(a)  # Step the environoment with the sampled random action
        episode_return += reward
        episode_len += 1
        if done:
            episode_done += 1
            break
    env.reset()
    print(f'Episode {i}_{episode_done}, cum. return: {episode_return:0.1f}, length: {episode_len}.')
    episode_name = f'Train_SAC_push.gif'
    save_gif(episode_name, episode_obs, dur)
    episode_return = 0
    episode_len = 0
    episode_obs = []
    
