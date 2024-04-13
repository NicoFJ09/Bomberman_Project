"""
Divide and conquer: Break down the game into smaller components, such as player movement, bomb placement, enemy behavior, level generation, and collision detection.

Use data structures: Instead of classes, use data structures like lists, dictionaries, and tuples to represent game entities and state.

Recursion for game logic: Use recursive functions to handle game logic, such as checking for collisions, resolving player movements, and updating the game state.

Design the game loop: Implement a game loop that repeatedly updates the game state, processes user input, and renders the game world using Pygame.

Level design: Design your levels using a simple grid-based approach. You can represent each level as a 2D array where each element corresponds to a tile type (empty space, wall, player, enemy, etc.).

Collision detection: Implement collision detection using recursive functions to check for collisions between players, enemies, bombs, and walls.

Rendering: Use Pygame to render the game world and display graphics. You can use recursive functions to draw the game world recursively, starting from the top-left corner and working your way through each tile.

Handle user input: Use Pygame's event handling system to process user input, such as keyboard or mouse events, and update the game state accordingly.

Implement game mechanics: Implement Bomberman's core mechanics, such as bomb placement, explosion propagation, enemy AI, power-ups, and level progression, using recursive functions and basic logic.

Testing and debugging: Test your game thoroughly and debug any issues that arise. Since you're not using OOP, debugging might involve carefully tracing the flow of your recursive functions and checking for logical errors.

"""

import pygame
import sys
sys.path.append('../')
from var_consts import *
from Screens.home import render_home

pygame.init()

#Window setup 
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode ((WIDTH,HEIGHT))

#Main Background
background = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Home_bg.png").convert_alpha(), (1200, 900))

#Font load
font = pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",50)

clock = pygame.time.Clock()

def main():
    current_screen = "start"
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #1 Home screen rendering
        if current_screen == "start":
            render_home(screen, background, font, WIDTH,HEIGHT)
        

        #Update
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()