# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:57:08 2020

@author: Aly
"""
# Firstly I import packages that I might need

from random import randint

from psychopy.visual import Window, ImageStim
from psychopy.event import getKeys, Mouse
from psychopy.clock import Clock

# I create a function which randomly changes the position of my target
# I chose numbers depending on my DISP size (I want the target to be always presented inside the screen)
# then the new position is set to the target, so the target can be moved

def move_target_at_random_pos(target):
    pos_x = randint(-700, 700)
    pos_y = randint(-400, 400)
    
    new_pos = (pos_x, pos_y)
    target.setPos(new_pos)
    
# I call out the objects I will use and define my DISP and BGC:
DISPSIZE = (1400,800)
BGC = (-1,-1,-1)
score = 0

win = Window(size=DISPSIZE, units='pix', fullscr=False, color=BGC)
target = ImageStim(win, 'target.png', size = (420, 420)) # i created this target in photoshop
mouse = Mouse(win)

mouse_click_clock = Clock()

# The game starts now by drawing the target at a random location:

move_target_at_random_pos(target)

while True:
    target.draw()  
    win.flip()
    
    # since I am still to develop the game, I give myself the option to stop it
    # at any time by pressing 'q' (avoiding the otherwise infinite loop)
    
    keys_pressed = getKeys()
    if 'q' in keys_pressed:
        break
  
    mouse_is_pressed = mouse.getPressed()[0] == True
    
    # Check for a mouse click every 0.2s, so that we don't accept more than 1
    # press on mouse hold
    if mouse_is_pressed and mouse_click_clock.getTime() > 0.2:
        mouse_click_clock.reset()
    
        if  mouse.isPressedIn(target):
            mouse_in_target = True
            # In the next version we'll use the score to
            # change the level when a certain threshold is hit
            score += 1
        else:
            mouse_in_target = False
        
        # either way we want to move the target (regardless if it is pressed on it or not)
        move_target_at_random_pos(target)


win.close()
