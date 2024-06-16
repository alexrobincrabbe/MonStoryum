[Monstoryum](https://monstoryum-24200bf7a5d2.herokuapp.com/) is a classic text RPG adventure game.
It is programmed in python to be played in the terminal.
The player begins in a room, locked in a jail cell, and must complete challenges in each room, defeating monsters in or to escape the dungeon. It has been deployed in a mock terminal.

Monstoryum was made as a project to showcase the Python skills of the website developer.

## Table of Contents
1. <details open>
    <summary><a href="#ux">UX</a></summary>

    <ul>
    <li><details>
    <summary><a href="#goals">Goals</a></summary>

    - [Visitor Goals](#visitor-goals)
    - [Business Goals](#business-goals)
    - [User Stories](#user-stories)
    </details></li>
</details>

2.  <details open>
    <summary><a href="#features">Features</a></summary>

    - [Intro screen](#intro-screen)
    - [Examine room screen](#examine-room-screeen)
    - [Inventory](#inventors)
    - [Status](#status)
    - [Target select](#select-target)
    - [Examine select](#examine-select)
    - [Hall of fame](#hall-of-fame)

</details>

3. <details open>
    <summary><a href="#technologies-used">Technologies Used</a></summary>

    - [Languages](#languages)
    - [Libraries](#libraries)
</details>

4. <details open>
    <summary><a href="#testing">Testing</a></summary>

    <ul>
    <li><details>
    <summary><a href="#validation">Validation</a></summary>

    - [pylint](#Pylint)
    - [flake8](#Flake8)
    </details></li>
    <li><details>
    <summary><a href="#bugs">Bugs</a></summary>

    - [Unfixed Bugs](#unfixed-bugs)
    - [Fixed Bugs](#fixed-bugs)
    </details></li>
    </li>
    </ul>
</details>

5. <a href="#future-improvements">Future Improvements</a>

6. <details>
    <summary><a href="#deployment">Deployment</a></summary>

    - [Clone Repository](#local-preparation)
    - [Deploy from Github](#local-instructions)
    
</details>

7. <details>
    <summary><a href="#credits">Credits</a></summary>

    - [Images](#images)
    - [sounds](#sounds)
    - [Code](#code)
    - [Testing](#testing)
</details>

----

# UX
## Goals
### Visitor Goals
The target audience for MonStoryum:
- The game is aimed at all fans of classic RPG games

User goals are:
- Have fun
- Be immersed in the story
- complete challenges, learn stategies to beat the game
- replay the game after playing all the way through

MonStoryum fills these needs by:
- Providing a challenging game
- Provind detailed descriptions of all rooms, monsters and items
- Providing a variety of challenges for the player to complete in each room
- Providing an extra optional challenge for the player before completing the game

### Business Goals
The Business Goals of MonStoryum are:
- Provide a fun game to engage visitors to the website
- Showcase the skills of the website owner

### User Stories
1. As a user, I expect to the game commands to be clear
2. I expect feedback on any input I enter
3. I expect to be able to check the status and inventory of my player
3. I expect to compare my results with other players at the end of the game

## Development
### logical flow
<div align="center">
  <img src="readme_images/flowchart.png">
</div>


### Process

The concept for the game was to have a linear set of rooms, with the option to only go forwards or backwards, in order to keep the scope manageable. 
I initially created the classes that I would need to create the game content. Since item objects are also attributes of other classes, I had to make the item class first.
Monsters and features are attributes of the room class, so needed to be created next.
Once these classes had been created, then the rooms could be created and populuated.
The Player and Dragon classes were added as extensions of the Monster class. The Player class adds methods relating to the inventory and status actions. The Dragon class adds a talk method, which calls the hangman game.
The hangman game was made as an independent game, for testing purposes and then imported to the main game. 
Due to the size of the program, the code was refactored into modules:
1. run.py calls the create game and enter room functions to start the game
2. create_game.py creates all of the classes and obects instances that are needed for the game, it monsters, items, features, rooms. As the Player class is an extension of the Monster class, it is also created here, and the player is prompted to enter a name
3. play_turn.py contains all of the functions that run once the game has started, with the exception of the endgame functions and clear_console function
4. endgame.py contains the functions that end the game, and updates the google sheet containing the Hall of Fame data
5. clear.py contains a function to clear the console
6. The other modules contain the classes used for the game

# Features

## intro screen

## examine room screen

## Status

## Inventory

## Target Select

## Exmamine Select

## Hall of Fame

# Technologies Used
## Languages
- Python

## Libraries
### Python modules
 #### Built in
- random
- math
- time
- os
- operator

#### Others
- rich
- prettytable
- gspread

## Platforms
- [Github](https://github.com/)
    * Storing code remotely
- [Gitpod](https://gitpod.io/)
    * IDE for project development
- [Heroku](https://heroku.com/)
    * Deployment

# Testing
## Validation

## Manual testing


## Bugs

### Unfixed Bugs

There are no unfixed bugs that I am aware of

### Fixed Bugs

The endgame functions originally called the main function to restart the game and break out of the start_turn loop. However after refactoring the code to modules, these causes a import recursion error. Therefore I refactored to code to exit the loop when the game had finished. This caused several bugs, where the game would continue the loop when it ended, or text was printed that should not appear on the screen. I had to fix these by introducing extra variables and condition checks to exit the loop when the game ended.

# Future Improvements

- add a room map, that updtes when the player explores

- add a seconds room index, so that the player has a choice of directions and the game is not linear

- add friendly monster mechanics

# Deployment
## local deployment

## Heroku

# Credits

Thanks to Leda for helping with the room descriptions
