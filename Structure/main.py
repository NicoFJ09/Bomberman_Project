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

from Screens.Levels.Level_1 import render_level_1

from Screens.settings import render_controls_volume

pygame.init()

#Window setup 
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((HWIDTH,HHEIGHT))

#Home Background
Hbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Home_bg.png").convert_alpha(), (HWIDTH,HHEIGHT))

#Menu Background
Mbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Menu_bg.png").convert_alpha(), (MWIDTH,MHEIGHT))
#Font load
font = pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",30)

#game ticks setup
clock = pygame.time.Clock()
blink= pygame.time.get_ticks()

#DETECTAR SALIR JUEGO

def handle_quit():
    # Check if there are events in the event queue
    if pygame.event.peek(pygame.QUIT):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Call handle_events recursively
        return handle_quit()

#DETECTAR MOVIMIENTOS EN HOME

def handle_home_controls(selected_index, options, selected_option):
    events = pygame.event.get()
    if not events:  # Base case: No more events
        return selected_index, selected_option
    
    event = events.pop(0)  # Get the first event
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:  # Move selection up
            selected_index = (selected_index - 1) % len(options)
        elif event.key == pygame.K_s:  # Move selection down
            selected_index = (selected_index + 1) % len(options)
        elif event.key == pygame.K_RETURN and current_screen=="home":  # Select option
            selected_option = options[selected_index]
            return selected_index, selected_option
        elif event.key == pygame.K_RETURN and current_screen=="settings":  # Select option
            selected_key = list(options.keys())[selected_index]
            selected_option = selected_key
            return selected_index, selected_option
            
    return handle_home_controls(selected_index, options, selected_option)

def handle_selected_option(selected_option):
    if selected_option == "START":
        return "level_1"  # Update current screen to level 1
    elif selected_option == "SETTINGS":
        return "settings"
    elif selected_option == "MANUAL":
        return "manual"
    elif selected_option == "TOP_SCORES":
        return "top_scores"
    elif selected_option == "ABOUT":
        return "about"
    elif selected_option == "MAIN MENU":
        return "home"
    elif selected_option in ["MOVE UP:", "MOVE DOWN:", "MOVE LEFT:", "MOVE RIGHT:",
                            "DROP BOMB:", "DETONATE BOMB:", "PAUSE:", "SOUND TOGGLE:",
                            "MUSIC TOGGLE:"]:
        return "settings"
    elif selected_option == "EXIT (APPLY CHANGES)":
        return "home"

def main():
    global selected_index, Settings_options, Home_options, selected_option, current_screen, blink, blink_interval, last_blink_time
    while RUNNING:
        # Handle exit after pressing x
        handle_quit()
        #1 Home screen rendering
        if current_screen == "home":
            selected_index, selected_option = handle_home_controls(selected_index, Home_options, selected_option)
            current_screen= handle_selected_option(selected_option)
            render_home(screen, Hbackground, font, HWIDTH,HHEIGHT,selected_index, Home_options)
        if current_screen == "settings":
                # Toggle blinking state based on timer
            current_time = pygame.time.get_ticks()
            if selected_option== list(Settings_options.keys())[selected_index] and current_time - last_blink_time > blink_interval:
                blink = not blink
                last_blink_time = current_time
            selected_index, selected_option = handle_home_controls(selected_index, Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            render_controls_volume(screen, Mbackground, Hbackground, font, HWIDTH, HHEIGHT, MHEIGHT, selected_index, Settings_options, blink)
        elif current_screen == "manual":
            pass
        elif current_screen == "top_scores":
            pass
        elif current_screen == "about":
            pass
        elif current_screen == "level_1":
            render_level_1(screen,font, HWIDTH, HHEIGHT)
        #Update
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()