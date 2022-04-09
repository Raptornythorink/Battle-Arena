# Battle Arena

# Description 

Our game features a main playable character fighting against successives waves of enemies.
He wields a magical sword that ominously floats around him.
He has a health bar and can move in a limited area delimited by walls. His goal to stay alive as long as possible by avoiding the attacks of enemies and eliminating them.
The enemies are of multiple kinds and also have their own life bars. They grant the player gold upon death. 
At the end of each wave, gold can be spent in the store to improve the character's characteristics. 
The game is over when your character runs out of health points or when you clear the last wave.
There are three levels of difficulty wich you can set in the options menu.
The difficulty changes the enemies's characteristics.

The character and the enemies are animated, there are sound effects and music.


# Starting the game

To start the game, you need to execute the file named "battle_arena.py" in the main folder.
The main menu appears, you can directly start playing by pushing the space button on your keyboard or open the options menu,
as indicated at the bottom of this menu.

# Gameplay basics

* Use the arrows on your keyboard to move your character (you can move diagonally).
* Enemies all appear at the same time at the beginning of a wave.
They will spawn randomly across the map, at a safe distance from the player.
* Use the space button to strike with your weapon. To deal damage you need to face an enemy. They drop gold upon death.
* In the shop, you can heal your character, increase his max health and his damage. You can save your money for the next time.
* You can buy an item only once (your can heal as many times as you want though).
* As indicated in the displayed window, you can navigate in this shop by using your keyboard arrows to switch between the different buttons, the Space key to buy an item (if possible), and the Enter key to close the shop.
* When you're done, press enter to play next wave. There is a five-second delay before the next wave.
* You can exit the game at any time by pressing the Escape key or by closing the window.
* See "gameplay details" for more information.

# Code 
Our code is divided in the following directories and files: 

## battle_arena.py
This file is meant for the execution of the game.


## Source

### game.py

In this file we call a class called Game in which we initialize our map. In this class we implement different functions to establish the initial mainloop. It is composed of:  
 __init__() uses the module pygame to display the gamescreen, the time clock (time between each frame),  
new() create new entities such as ennemies, wave ennemies, walls, weapons, life bars that are used throughout the game.
run() which is the mainloop
events() which recover pressed keys  
update() wich updates the entities like lifebars, waves, sprites.  
draw() wich displays the different sprites on the screen.
quit() wich quits the game.
lost() wich handles the death of the player and calls the dedicated menu.
And a last function called won() that handles victory and calls the dedicated menu.
   

### waves.py

This file defines a class called Wave which allows to spawn a wave of ennemies. Once all of them are dead, the shops appears. The player has 5 seconds after finishing buying items before the next wave appears.

## Settings

### settings.py 
Here we have all of the constants that we'll need in the project. We have the constants defining our Window, the player attributes, the weapons attributes, the ennemy attributes...

## Entities

### player.py

In a class called Player we wrote different functions that modelise our main character.  
We initialize first by using ppygame the player in a __init__ function.  
Then in a another function called move() we configure the different deplacement of our main character,  
Then in two function called hurt and heal we respectively Lowers the player's hp(hit point = life point) and increase the player's hp,  
Then in a function called in_attack_range() we verify wether or not an ennemy is in the attack range of the main character,  
Then in a function called attack() that makes player attacks in the direction he faces. 
And lastly a function called update_pl_facing() that update the direction the player faces. 
 
### entities.py 

Basically manages the enemies, as well as the walls.
We create an enemy by using pygame in a __init__ function,  
move_ennemy() we move the enemy towards the player.  
knockbacks_enemy_player() to make the enemy knock back when it collides with the main character.
knockbacks_enemy_wall() to push the enemy away from a wall, pixel by pixel. 
hurt() lowers the ennemies hp.
And last the function update_enemy() that update the enemy's position.

Other classes are in this files such BaseEnemy or BossEnemy to modify the type of enemy the character faces.
Those classes encompasses several different sprites, animated and displayed on the screen for each specific enemy.

### lifebar.py
This file initializes the life bars of the player and the ennemies. The lifebar is a green bar. When it decreases, it is replaced by a red bar. This occurs whenever the ennemy or the main character is hit.

### player_model.py
This file transforms the main character which was a rectangle until now into an animated model.

### spritesheet.py

This file defines a class and a fonction designed to fetch a frame of a sprite contained into a spritesheet.


## Menus

### starting_menu.py
This file displays the game menu to start the game and it also sets the desired settings (difficulty).

### interwave_menu.py
This file designs the menu displayed between two waves. The player can eitehr keep his gold points and go to the next
wave or spend earned money into new weapons (more attack damage) or new protections (more max health).

## SoundEffects

### Sounds

This repository contains all of the sound effects and music used in the game.

### sounds.py

This file defines two classes which handle the music and sound effects files.

## Sprites

This file contains all of the sprites used for entity animations.

## Textures

### map_tiled.tmx
This file is a xml file used to display the background of the game.

### RPG_16x16.tsx

This file is referenced by map_tiled.tmx in order to load the correct textures.

### Pipoya RPG Tileset 16x16

This repository contains all of the textures that are used in the map (and more).
It is refrenced by RPG_16x16.tsx.


## Tests


### test_functions.py

This file contains different tests made to check that our fonctions work as intended.



# Gameplay details

* You start with 20 hp and 5 atk damage
* There are 4 types of enemies : basic, tank (slow, no knock back, high damage, hp and loot), rush (fast, low damage, hp and loot) and  
  boss (high damage, no knock back, extreme hp and loot)
* For instance in the medium difficulty, base enemies have 20hp, rush have 10 and boss has 200. You can see details in the settings file.
* When buying an armor, your current hp will increase so that your % of current hp stays the same. Protip: heal before buying armor.
* You can only buy up to one exemplary of the same item. More expensive armors give more hp per gold spent.
* Buying a weapon will replace your current atk with the weapon's one (if it increases it) : you can't just accumulate weapons.
* The area affected by a player's attack is a square with the player at the center of one side.
* Your score is the total gold earned throughout the entire game.

# Team :

- Pierre CLAIRIN
- Aymeric CHAUMONT
- Ryad GUEZZI
- Muriel KENMOGNE
- Mohamed NDIAYE
- Hugo KHLAUT
