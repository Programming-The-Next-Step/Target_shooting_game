# Target_shooting_game

## Project Description

# About the game
In this project I aim to build a game in which the user ‘shoots’ at a target on the screen by using a mouse-click. Once the user successfully clicks on the target, the target will move to a new random location on the screen. Should the user not clock at all, the target will automatically move after **X** seconds. The player will start the game with _**3 lives**_ and _**0 points**_. A point is obtained by successfully clicking on the target. A life is lost when the player either doesn’t click at all or misses the target. Once the player reaches 5 points, the level increases, meaning the target automatically moves to a new location faster. Same goes if the player reaches 10 points. The game finishes after the player reaches 15 points or if the player’s lives drop to 0. At the end of the game, the player can see an overview of each of the three levels with dots marking where (in the target) the player shoot at each level. This information can also be obtained in a csv file. The goal of the game is to track the reaction time of the user. I hope it will be a fun game!

# Building the game
To build this game I will first start with the basics – making my own target and showing it on the screen, randomizing it’s movements and making sure that it moves after a certain amount of time or after it is clicked with the mouse. Should I not have enough time to implement everything, possibly I will cut on the overview of the levels and just save the information in the csv file instead. If I have more time than anticipated, I can work on developing the levels and measuring reaction time (also to be saved on the csv file). 

# What will I use?
For programming this game I plan to use **Python** with the following packages: random and psychopy (visual, core, event, clock). I plan to create a function that randomly resents a target to a new position and draws it there. Additionally, a similar function should be created for the final overview with 3 targets next to each other (for each level) and the successful hits in each target.




