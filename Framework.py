# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:40:07 2020

@author: Rilind
"""

import random
import numpy as np

def ones(size):
    to_return = []
    for i in range(size):
        to_return.append(1)
    return to_return


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

print("Welcome to Mastermind.")

# Game Parameters
CODE_PEG_SELECTION_COUNT = 4
MAX_GUESSES = 10
code_pegs = [BLUE, RED, GREEN, YELLOW, PURPLE, BROWN]

# Array to store the code we need to find
code_to_crack = []

# Add random colours to the code we need to find
for i in range(CODE_PEG_SELECTION_COUNT):
    code_to_crack.append(random.randint(0, len(code_pegs) - 1))
    
#print(code_to_crack)
    
print("Code of length %s has been set, what is your guess?" % (CODE_PEG_SELECTION_COUNT))

num_tries = 0
while(num_tries < MAX_GUESSES):
    # Array to store the guesses
    code_guess = []
    
    # Store each guess one by one into the array
    for i in range(CODE_PEG_SELECTION_COUNT):
        # TODO: Try/catch ValueError
        code_guess.append(int(input("Guess %s:" % (i + 1))))
       
    # Output pegs stored here
    key_pegs = []
    
    # Place a black peg if we get colour and position correct
    # Place a white peg if we get colour correct and position wrong
    for i in range(len(code_guess)):
        guess = code_guess[i]
        if guess == code_to_crack[i]:
            key_pegs.append(BLACK)
        elif guess in code_to_crack:
            key_pegs.append(WHITE)
        else:
            key_pegs.append(NOTHING)
    
    # Shuffle the position of the pegs and feedback
    random.shuffle(key_pegs)
    print(key_pegs)
    
    if key_pegs == ones(CODE_PEG_SELECTION_COUNT):
        print("Great job! It took you %s tries" % (num_tries))
        break
        
    
    num_tries += 1
    

if num_tries == MAX_GUESSES:
    print("Out of tries! The correct code was: %s" % (code_to_crack))
        




