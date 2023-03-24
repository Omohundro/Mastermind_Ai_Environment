# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:54:35 2021

@author: Rilind
"""

import gym
from gym import spaces
import numpy as np
from random import randrange
import random
import math

MAX_GUESSES = 10
BOARD_SIZE = 5

# Code pegs
BLUE = 0
RED = 1
GREEN = 2
YELLOW = 3
PURPLE = 4
BROWN = 5

# Key pegs
NOTHING = -1
WHITE = 0
BLACK = 1

CODE_PEG_SELECTION_COUNT = 4
code_pegs = [BLUE, RED, GREEN, YELLOW, PURPLE, BROWN]

code_to_crack = []

class MastermindEnvironment(gym.Env):
    
    def __init__(self, config = None):
        self.board = np.zeros((BOARD_SIZE,), dtype=int)
        # assuming this will fill every slot on the board with zeros
        self.action_space = spaces.MultiDiscrete([len(code_pegs), len(code_pegs), len(code_pegs), len(code_pegs)])
        # observation space will be (10, 8) - so an array of 10 rows and 8 columns
        self.observation_space = spaces.Box(low=-len(code_pegs), high=len(code_pegs),
                                        shape=(MAX_GUESSES, BOARD_SIZE), dtype=np.float32)
        
        self.viewer = None
        self.last_action = None
        self.goal = None
        self.log_info = {}
        
    def reset(self):
        self.log_info = {
            "goal": self.goal,
            "last_action":self.last_action,
            "board":self.board
        }
        # Make the goal random on each episode
        self.goal = self.action_space.sample()
        self.num_tries = 0
        self.last_action = None
        self.board = np.zeros((10, BOARD_SIZE), dtype=int)
        return self.board
    
    def step(self, action):
        # print("The code guess is %s " % (action))
        self.last_action = action
        reward = -1
        for i in range(len(action)):
            self.board[self.num_tries][i] = action[i]
        # Add code pegs
        code_pegs = []
        
        # code_pegs.append...
        goal_copy = list(self.goal.copy())
        
        for i in range(len(action)):
            guess = action[i]
            if guess == goal_copy[i]:
                #print("Found exact %s at pos %s in %s" % (guess, i, goal_copy))
                code_pegs.append(BLACK)
                goal_copy[i] = -2
            elif guess in goal_copy:
                code_pegs.append(WHITE)
                #print("Found %s in %s, replacing -" % (guess, goal_copy))
                goal_copy[goal_copy.index(guess)] = -2
                #print("replaced with %s " % goal_copy)
            else:
                #print("Didn't find %s in %s" % (guess, goal_copy))
                code_pegs.append(NOTHING)
            #print("Pegs: %s" % code_pegs)
        
        # Code pegs are shuffled
        random.shuffle(code_pegs)
        # print(code_pegs)
        
        # set pegs into board
        self.board[self.num_tries][4] = sum(code_pegs)
        # self.board[self.num_tries][4] = code_pegs[0]
        # self.board[self.num_tries][5] = code_pegs[1]
        # self.board[self.num_tries][6] = code_pegs[2]
        # self.board[self.num_tries][7] = code_pegs[3]
        
        self.num_tries += 1
        
        if (self.num_tries == MAX_GUESSES) or (list(action) == list(self.goal)):
            done = True
        else:
            done = False
            
        if list(action) == list(self.goal):
            reward = 10
            
        #print(self.board)
        
        return(self.board, reward, done, {})
        
    def render(self, mode='human'):
        print("--------------")
        print("Guess %s Goal %s" % (self.last_action, self.goal))
        print(self.board)
        
        #from gym.envs.classic_control import rendering
        
        
    # def render(self, mode='human', board = None):
    #     if board is None:
    #         board_to_render = self.board
    #     else:
    #         board_to_render = board
            
        
    #     screen_width = 600
    #     screen_height = 800
    #     print(self.board)
        
    #     from gym.envs.classic_control import rendering
        
    #     if self.viewer is None:
    #         self.viewer = rendering.Viewer(screen_width, screen_height)
            
    #         # Column lines
    #         l, r, t, b = 75, 80, 0, 800
    #         column_one = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_one)
            
    #         l, r, t, b = 150, 155, 0, 800
    #         column_two = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_two)
            
    #         l, r, t, b = 225, 230, 0, 800
    #         column_three = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_three)
            
    #         l, r, t, b = 300, 305, 0, 800
    #         column_four = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_four)
            
    #         l, r, t, b = 375, 380, 0, 800
    #         column_five = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_five)
            
    #         l, r, t, b = 450, 455, 0, 800
    #         column_six = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_six)
            
    #         l, r, t, b = 525, 530, 0, 800
    #         column_seven = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(column_seven)
            
            
    #         # Row lines
            
    #         l, r, t, b = 0, 600, 70, 75
    #         row_one = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_one)
            
    #         l, r, t, b = 0, 600, 140, 145
    #         row_two = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_two)
            
    #         l, r, t, b = 0, 600, 210, 215
    #         row_three = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_three)
            
    #         l, r, t, b = 0, 600, 280, 285
    #         row_four = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_four)
            
    #         l, r, t, b = 0, 600, 350, 355
    #         row_five = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_five)
            
    #         l, r, t, b = 0, 600, 420, 425
    #         row_six = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_six)
            
    #         l, r, t, b = 0, 600, 490, 495
    #         row_seven = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_seven)
            
    #         l, r, t, b = 0, 600, 560, 565
    #         row_eight = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_eight)
            
    #         l, r, t, b = 0, 600, 630, 635
    #         row_nine = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_nine)
            
    #         l, r, t, b = 0, 600, 700, 705
    #         row_ten = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
    #         self.viewer.add_geom(row_ten)
            
            
            
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
            
            
            
        
        
        
        
        
        
        
        
        
    