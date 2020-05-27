# -*- coding: utf-8 -*-
"""
Created on Wed May 27 11:17:33 2020

@author: Aly
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:59:27 2020

@author: Aly
"""
from random import randint
from math import sqrt

from psychopy.visual import Window, ImageStim, TextStim, Circle
from psychopy.core import wait
from psychopy.event import getKeys, Mouse
from psychopy.clock import CountdownTimer, Clock
from psychopy import gui


# I create a function which randomly changes the position of my target
# I chose numbers depending on my DISP size (I want the target to be always
# presented inside the screen), then the new position is set to the target, 
# so the target can be moved
def move_target_at_random_pos(target):
    pos_x = randint(-700, 700)
    pos_y = randint(-400, 400)
    
    new_pos = (pos_x, pos_y)
    target.setPos(new_pos)
    

# Now I create a function that will draw 3 targets - one for each level of the game
# On these targets I want to show where the player clicked (scored) on each level
def draw_overview_target(target_x, target_y, mouse_clicks):
    target = ImageStim(win, 'target.png', size = 420, pos=(target_x, target_y))
    target.draw()
    
    for target_hit_pos in mouse_clicks:
        if target_hit_pos['mouse_in_target']:
            circle = Circle(win, radius=5, fillColor='yellow', lineColor='yellow')
            circle.setPos((target_hit_pos['mouse_x']+target_x, target_hit_pos['mouse_y']+target_y))
            circle.draw()

# Since psychopy reads my target image as a square and not a circle, sometimes
# a hit outside of the target is recorded as inside the target (as it is
# inside the image). Therefore, we want to ensure that a point is given 
# only when the player succesfully hits the target. We use the radius of the 
# circle to find the distance between the centre of the target and the hit
def distance_between_two_points(ax, ay, bx, by):
    return sqrt((ay - by)**2 + (ax - bx)**2)


def mouse_clicked_in_target(mouse, target):
    mouse_x, mouse_y = mouse.getPos()
    target_x, target_y = target.pos
    # size returns width and height, since the target image is
    # a square, it doesn't matter which one we pick
    radius = target.size[0] / 2
    distance = distance_between_two_points(mouse_x, mouse_y, target_x, target_y)
    
    return distance <= radius # we make sure the distance is not longer than
                              # the radius

# Now I create a function that will help us save these results in a csv file
def write_results(target_hits_per_level, filename):
    with open(filename, 'w') as file: # when with open --> file is closed automatically at the end
        file.write('Level,mouse_X,mouse_Y,reaction_time,mouse_in_target\n')
        
        for level_index, level_clicks in enumerate(target_hits_per_level):
            level = level_index + 1
        
            for mouse_click in level_clicks:
                mouse_x = mouse_click['mouse_x']
                mouse_y = mouse_click['mouse_y']
                reaction_time = mouse_click['reaction_time']
                mouse_in_target = mouse_click['mouse_in_target']
            
              
                file.write(
                    str(level) + ',' +
                    str(mouse_click['mouse_x']) + ',' +
                    str(mouse_click['mouse_y']) + ',' +
                    str(mouse_click['reaction_time']) + ',' +
                    str(mouse_click['mouse_in_target']) + '\n'
                )


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

# I set up my siplay size and background colour
DISPSIZE = (1400, 800)
BGC = (-1,-1,-1)

DISPLAY_WIDTH = DISPSIZE[0]
DISPLAY_HEIGHT = DISPSIZE[1]

LIVES_X = -DISPLAY_WIDTH / 2
LIVES_Y = DISPLAY_HEIGHT / 2


# for my game I need to create some variables:
score = 0
lives =  3
level = 1
mouse_x = 0
mouse_y = 0


# I create some objects:
win = Window(
    size = DISPSIZE,
    units = 'pix',
    fullscr = False,
    color = BGC
    )

mouse = Mouse(win)

target = ImageStim(
    win,
    'target.png',
    size = (420, 420)
    )

# I will display three text stimuli to the player while playing the game:
lives_count = TextStim(
    win,
    text = f'Lives = {lives}',
    height=35,
    color = (1,0.2,0.6),
    pos = (100, 330),
    )

score_count = TextStim(
    win, 
    text = f'Score = {score}', 
    height = 35, 
    color = (0.2,0.2,0.8), 
    pos = (450,330)
    )

level_count = TextStim(
    win, 
    text = f'Level = {level}', 
    height = 35,
    color = (1, -0.5, 1), 
    pos = (850, 330)
    )

# I define the messages to show the player the outcome of the game:
you_have_lost = TextStim(
    win, 
    text = 'Boo! Not a great game, pal... Get it together!', 
    height = 35, 
    color = (0.2,0.2,0.8), 
    pos = (250,230)
    )

you_have_won = TextStim(
    win, 
    text = 'Yey! Well done, champ! Time to celebrate!', 
    height = 35, 
    color = (0.2,0.2,0.8), 
    pos = (250,230)
    )

# These are the images I use for the winning and loosing scenarios:
looser = ImageStim(
    win,
    'failed.jpg',
    pos = (0,-100),
    size = (420,420)
    )
winner = ImageStim(
    win,
    'tiny_trash.jpg',
    pos = (0,-100),
    size = (420,420)
    )


# I introduce this dialog to save the user's ID:
user_id_dialog = gui.Dlg(title="Target Game")
user_id_dialog.addText('Please write your subject ID: a 4-digit code')
user_id_dialog.addField('Subject ID:')
ok_data = user_id_dialog.show()  # show dialog and wait for OK or Cancel

if not user_id_dialog.OK:
    print('user cancelled')



# NOW THE GAME WILL START:

# If enabled, intro will play:
enable_intro = True

if enable_intro:
    show_intro(win)

# We create this list to save our results into
target_hits_per_level = [
    [],
    [],
    [],
    [],
]

move_target_at_random_pos(target) # first the target is shown on the screen

lives_timer = CountdownTimer(5) # Level 1 starts with 5 sec to hit the target
mouse_click_clock = Clock()
reaction_time_clock = Clock()
change_target = False

while level < 4 and lives > 0:
    target.draw()
    target_x, target_y = target.pos
    lives_count.draw()
    score_count.draw()
    level_count.draw()
    
    win.flip()
    
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
        mouse_in_target = None 
        mouse_in_target_x = None
        mouse_in_target_y = None
        change_target = True

    # Check for a mouse click every 0.2s, so that we don't accept more than 1
    # press on mouse hold
    if mouse_is_pressed and mouse_click_clock.getTime() > 0.2:
        mouse_click_clock.reset()
        
        if mouse_clicked_in_target(mouse, target):
            mouse_in_target = True
            mouse_in_target_x = mouse_x - target_x
            mouse_in_target_y = mouse_y - target_y
            score += 1
            score_count.setText(f'Score = {score}')
            
                     
            
            if score == 5:
                lives_timer.reset(3)
                level = 2 
                print(f'Level = {level}')
            elif score == 10:
                lives_timer.reset(1)
                level = 3   
            elif score == 15:
                level = 4
        else:
            lives -= 1  #player looses a life also if he/she clicks outside the target
            lives_count.setText(f'Lives = {lives}')
            mouse_in_target = False
            mouse_in_target_x = None
            mouse_in_target_y = None
            
        change_target = True
    
    if change_target:
        
        mouse_click = {
                     'mouse_x': mouse_in_target_x,
                     'mouse_y': mouse_in_target_y,
                     'reaction_time': reaction_time_clock.getTime(),
                     'mouse_in_target': mouse_in_target,
                     } 
        target_hits_per_level[level-1].append(mouse_click) # inddexes start from 0 --> level - 1
        
        move_target_at_random_pos(target)
        lives_timer.reset()
        reaction_time_clock.reset()
        change_target = False
     

# Here we display the outcome of the game:
if level == 4:
    you_have_won.draw()
    winner.draw()
    win.flip()
    wait(3)
else:
    you_have_lost.draw()
    looser.draw()
    win.flip()
    wait(3)


# Finally, we draw the overwivew for thr player

# HERE I know that I create 3 almost identical text messages,
# so I might take this one out in a function, but I did not have time
level_1 = TextStim(
    win,
    text = 'Level 1',
    height = 35,
    color = (0.2,0.2,0.8),
    pos = (50,330)
    )

level_2 = TextStim(
    win,
    text = 'Level 2',
    height = 35,
    color = (0.2,0.2,0.8),
    pos = (450,330)
    )

level_3 = TextStim(
    win,
    text = 'Level 3',
    height = 35,
    color = (0.2,0.2,0.8),
    pos = (850,330)
    )

level_1.draw()
level_2.draw()
level_3.draw()
draw_overview_target(-450,0, target_hits_per_level[0])
draw_overview_target(0, 0, target_hits_per_level[1])
draw_overview_target(450, 0, target_hits_per_level[2])
win.flip()
wait(3)

# The user has not clicked Cancel on the subject ID window
if ok_data is not None:
    write_results(target_hits_per_level, 'results-' + ok_data[0] + '.csv')

win.close()
