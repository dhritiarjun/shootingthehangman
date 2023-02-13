# shootingthehangman
Python Project: Hangman with a Twist
Dhriti Arjun, Nora Bongaardt, Hannah Fritsch
November 2022

Idea: Our initial idea involved coding a game based on a Hangman, because all three of us love Halloween and horror games, 
and there is nothing scarier than an executioner (in our opinion).  Further, all three of us had played those classic arcade style shooter games 
when we were young, and thought it could be a cool idea for a project to make an arcade style shooter game with a Hangman as the enemy. 

Strategy: We coded the arcade game in pygame (because this was easier and all online research suggested this) and this worked reasonably well.  
We did this by using inspiration from existing but different shooting games to help us learn pygame and its syntax, and by using resources like books and Google 
to help us solve the problems that came up along the way. 

Process: We worked on this project intensively for the full four weeks, often spending hours on troubleshooting and figuring out what the problems were.  
We found it quite difficult to quickly put our project together, because we had to familiarise ourselves with completely new python libraries (like pygame).  
It was a long, arduous and difficult process, but by helping each other we managed to fulfil the criteria of the project and code a good game.

USER MANUAL

The aim of the game is to avoid the evil Hangman, who is trying to shoot the user’s character, and shoot him first.  If the user shoots the evil Hangman first, the user wins.

Use the arrow keys to move (left, right, up and down) and press the spacebar to shoot.  The character can move all around the screen.

The user is first welcomed by a menu screen, from which they have three choices:

Play: Will take the user to the game
Description: Will show the user a short description of the game.
Quit: Quits the game

After the game ends, the user is shown a win or a lose screen.  Both will give the user the option to go back to the menu screen and try again, or quit the game.  Please note that these screens will take a second to load; this is normal.

To open the game, change the directory to Final_AP_Project and run 'main.py'.

Please note that our code runs with pythonw, so the function that kills the existing screen and spawns another screen is made using pythonw. 
If your device uses python3 or python commands in the terminal this needs to be changed in the code.
