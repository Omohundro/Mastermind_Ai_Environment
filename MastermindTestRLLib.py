# -*- coding: utf-8 -*-
#%% Imports and definitions
import ray
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.ppo import ppo
from ray.rllib.agents.impala import impala
from ray.rllib.agents.impala import ImpalaTrainer


import os

from MastermindEnvironment import MastermindEnvironment as mastermind


#%% Train agent
config = impala.DEFAULT_CONFIG

config['num_workers'] = 12
config['num_gpus'] = 1

ray.init(ignore_reinit_error=True)
agent1 = ImpalaTrainer(env=mastermind, config=config)

while True:
    agent1.train()
    
    
#%% Save agent
name = "rllib_ppo" 
    
try:
    os.mkdir(name)
except OSError:
    print ("Creation of the directory %s failed" % name)
else:
    print ("Folder %s already exists" % name)
 
agent1.save_checkpoint("%s" % name)

