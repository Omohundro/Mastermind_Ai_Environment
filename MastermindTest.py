# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:10:05 2021

@author: Rilind
"""


# %% imports and definitions
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import set_global_seeds, make_vec_env

from stable_baselines import PPO2
from stable_baselines import A2C
from stable_baselines import ACER
from stable_baselines import TRPO
from MastermindEnvironment import MastermindEnvironment as mastermind
from stable_baselines.common.vec_env import SubprocVecEnv
import time
import gym
import numpy as np


# %% learning
env = make_vec_env(mastermind, n_envs=16)
# env = mastermind()

model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log="./logs")
model.learn(total_timesteps=1000000000, tb_log_name="mastermind_ppo2_sum_fix")

model.save("ppo2_mastermind_sum_fix")

model = PPO2.load("ppo2_mastermind_sum_fix")

#del model

# %% testing
obs = env.reset()
rews = []
for i in range(1000):
    env.envs[0].render()
    time.sleep(1)
    action, _states = model.predict(obs, deterministic=False)
    #print(action)
    obs, rewards, dones, info = env.step(action)
    print("Reward: %s" % rewards[0])
    rews.append(rewards[0])
    if dones[0]:
        print("Final board state:")
        print(env.envs[0].log_info['board'])
        print(rews)
        rews = []
        
    
env.close()

