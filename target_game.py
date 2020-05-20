# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:57:08 2020

@author: Aly
"""
# Firstly I import packages that I might need

from random import randint

from psychopy.visual import Window, ImageStim, Circle, TextStim
from psychopy.event import getKeys, Mouse
from psychopy.clock import Clock, CountdownTimer
from psychopy.core import wait
#from psychopy import gui


# I create a function which randomly changes the position of my target
# I chose numbers depending on my DISP size (I want the target to be always presented inside the screen)
# then the new position is set to the target, so the target can be moved

def move_target_at_random_pos(target):
    pos_x = randint(-700, 700)
    pos_y = randint(-400, 400)
    
    new_pos = (pos_x, pos_y)
    target.setPos(new_pos)
    

# Now I create a function that will draw 3 targets - each for each level of the game
# On these targets I want to show where the player clicked (scored) on each level
def draw_overview_target(target_x, target_y, mouse_clicks):
    target = ImageStim(win, 'target.png', size = (420, 420), pos=(target_x, target_y))
    target.draw()
    
    for target_hit_pos in mouse_clicks:
        circle = Circle(win, radius=5, fillColor='yellow', lineColor='yellow')
        circle.setPos((target_hit_pos['mouse_x']+target_x, target_hit_pos['mouse_y']+target_y))
        circle.draw()

# Here I create a function for the intro, which allows me to explain the game to the participant
def show_intro(win):
    start = TextStim(
        win,
        text = "Hi there, player! This is you! Let's play!",
        height = 35,
        color = (0.2,0.2,0.8),
        pos = (250,230),
    )
    
    player = ImageStim(
        win,
        'creature.jpg',
        pos = (0,-100),
        size=(420,420),
    )
    
    intro_text = (
        'In this game you should shoot at the target with your mouse. '
        + 'The target moves rapidly to a new position each time you shoot at it.' 
        + 'There are 3 levels each faster than the previous one. Good luck!'
    )
    
    instructions = TextStim(
        win,
        text = intro_text,
        height = 35,
        color = (1, 0.2, 0.6),
        pos = (250, 0),
    )
    
    start.draw()
    player.draw()
    win.flip()
    wait(3)
    instructions.draw()
    win.flip()
    wait(8)           
    
    
# I call out the objects I will use and define my DISP and BGC:
DISPSIZE = (1400, 800)
# DISPSIZE = (GetSystemMetrics(0),GetSystemMetrics(1)) we can use this later on,
# but for now we need to build the programme
BGC = (-1,-1,-1)


score = 0
lives =  3
level = 1
mouse_x = 0
mouse_y = 0

win = Window(size=DISPSIZE, units='pix', fullscr=False, color=BGC)
target = ImageStim(win, 'target.png', size = (420, 420)) # i created this target in photoshop
mouse = Mouse(win)



lives_count = TextStim(win, text = f'Lives = {lives}', height = 35, color = (1,0.2,0.6), pos = (-50,330))
score_count = TextStim(win, text = f'Score = {score}', height = 35, color = (0.2,0.2,0.8), pos = (450,330))
level_count = TextStim(win, text = f'Level = {level}', height = 35,color = (1, -0.5, 1), pos=(850, 330))



#we need this for the overview at the end of the game
target_hits_per_level = [
    [],
    [],
    [],
    [],
]


enable_intro = True #I enable the intro
# We allow this option for easier checks of the programme (e.g. if we 
#do not want to watch the intro but skil to the game)

if enable_intro:
    show_intro(win)

lives_timer = CountdownTimer(5) # Level 1 starts with 5 sec to hit the target
mouse_click_clock = Clock()
reaction_time_clock = Clock()


# The game starts now by drawing the target at a random location:

move_target_at_random_pos(target)


mouse_click_clock = Clock()

while level < 4 and lives > 0:
    target.draw()
    reaction_time_clock.reset()
    target_x, target_y = target.pos
    lives_count.draw()
    score_count.draw()
    level_count.draw()
    
    win.flip()
    
    # since I am still to develop the game, I give myself the option to stop it
    # at any time by pressing 'q' (avoiding the otherwise infinite loop)
    
    keys_pressed = getKeys()
    if 'q' in keys_pressed:
        break
  
    mouse_is_pressed = mouse.getPressed()[0] == True
    mouse_x, mouse_y = mouse.getPos()
    
    level_count.setText(f'Level = {level}')
    
    
    #if the player does not click, the target moves and the player looses a life
    if lives_timer.getTime() <= 0: 
        lives -= 1
        lives_count.setText(f'Lives = {lives}')
        move_target_at_random_pos(target)
        lives_timer.reset()
    
    # Check for a mouse click every 0.2s, so that we don't accept more than 1
    # press on mouse hold
    if mouse_is_pressed and mouse_click_clock.getTime() > 0.2:
        mouse_click_clock.reset()
    
        if mouse.isPressedIn(target):
            mouse_in_target_x = mouse_x - target_x
            mouse_in_target_y = mouse_y - target_y
            score += 1
            score_count.setText(f'Score = {score}')
            
            if score == 5:
                lives_timer.reset(3)
                level = 2        
            elif score == 10:
                lives_timer.reset(1)
                level = 3   
            elif score == 15:
                level = 4
                
            mouse_click = {
                'mouse_x': mouse_in_target_x,
                'mouse_y': mouse_in_target_y,
            }
            
            target_hits_per_level[level-1].append(mouse_click)# inddexes start from 0 --> level - 1
        else:
            lives -=1 #player looses a life also if he/she clicks outside the target
            lives_count.setText(f'Lives = {lives}')
            
        # either way we want to move the target (regardless if it is pressed on it or not)
        move_target_at_random_pos(target)

draw_overview_target(-450, 0, target_hits_per_level[0])
draw_overview_target(0, 0, target_hits_per_level[1])
draw_overview_target(450, 0, target_hits_per_level[2])
win.flip()
wait(3)

win.close()
