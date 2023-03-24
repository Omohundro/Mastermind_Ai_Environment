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
from stable_baselines import ACKTR
from MastermindEnvironment import MastermindEnvironment as mastermind
from stable_baselines.common.vec_env import SubprocVecEnv
import time
import gym
import numpy as np


# %% learning
env = make_vec_env(mastermind, n_envs=16)

model = A2C(MlpPolicy, env, verbose=1, tensorboard_log="./logs")
model.learn(total_timesteps=500000000, tb_log_name="mastermind_a2c")

model.save("a2c_mastermind")

model = A2C.load("a2c_mastermind")


# %% Create Testing Suite
import pickle

env = mastermind()
suite_size = 100

test_suite = []

for i in range(suite_size):
    test = env.action_space.sample()
    test_suite.append(test)
    
with open('test_suite.pickle', 'wb') as handle:
    pickle.dump(test_suite, handle, protocol=pickle.HIGHEST_PROTOCOL)

# %% testing

import pickle
# Load in test suite
with open('test_suite.pickle', 'rb') as handle:
    test_suite = pickle.load(handle)

env = make_vec_env(mastermind, n_envs=1)
model_name = "a2c_mastermind_sum"

model = A2C.load(model_name)

episode_rewards = []
episode_lengths = []

for i in range(len(test_suite)):
    print("Test %s" % (i+1) )
    obs = env.reset()
    env.env_method("set_test_goal", test_suite[i])
    done = False
    rews = []
    l = 0
    while not done:
        #env.envs[0].render()
        #time.sleep(1)
        action, _states = model.predict(obs, deterministic=True)
        #print(action)
        obs, rewards, dones, info = env.step(action)
        done = dones[0]
        l += 1
        
        #print("Reward: %s" % rewards[0])
        rews.append(rewards[0])
        if dones[0]:
            # print("Final board state:")
            # print(env.envs[0].log_info['board'])
            # print(rews)
            episode_rewards.append(sum(rews))
            episode_lengths.append(l)
            rews = []
            
wins = 0

for i in range(len(episode_rewards)):
    if episode_rewards[i] > -10:
        wins += 1
        
print("wins %s average len %s" % (wins, np.mean(episode_lengths)))

env.close()

