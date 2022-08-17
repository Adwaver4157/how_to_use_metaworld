from metaworld.envs.mujoco.sawyer_xyz.v2.sawyer_push_v2 import SawyerPushEnvV2
from metaworld.envs.asset_path_utils import full_v2_path_for

class SawyerPushEnv_ChangeV2(SawyerPushEnvV2):
    def __init__(self, seed=None):
        
        if seed is not None:
                st0 = np.random.get_state()
                np.random.seed(seed)
        super().__init__()
        self._partially_observable = False
        self._freeze_rand_vec = False
        self._set_task_called = True
        self.reset()
        self._freeze_rand_vec = True
        if seed is not None:
            self.seed(seed)
            np.random.set_state(st0)
        self.random_init = True
    
    @property
    def model_name(self):
        return self.model_path
    
    def step(self, action):
        if self.curr_path_length == self.max_path_length:
            observation, reward, done, info = super().step(action)
            return observation, reward, True, info
        else:
            observation, reward, done, info = super().step(action)
            return observation, reward, done, info
    
    def render(self, offscreen=False, camera_name="corner2", resolution=(640, 480)):
        if not offscreen:
            self._get_viewer('human').render()
        else:
            return self.sim.render(
                *resolution,
                mode='offscreen',
                camera_name=camera_name
            )
    
    @property
    def model_name(self):
        return full_v2_path_for('sawyer_xyz/sawyer_push_v2.xml')
    