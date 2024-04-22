import pygame
from var_consts import *

def handle_player_actions(Settings_options, player_position, is_moving, current_direction, blocks_positions):
    # By default, no movement
    dx, dy = 0, 0

    # Check if any movement keys are held down
    keys = pygame.key.get_pressed()

    if keys[pygame.key.key_code(Settings_options["PAUSE:"])]:
        return player_position, "PAUSED", False, current_direction
    elif keys[pygame.key.key_code(Settings_options["RESTART:"])]:
        return [240,60], "RESTART (A LIFE WILL BE LOST)", False, "RIGHT"

    elif keys[pygame.key.key_code(Settings_options["MOVE UP:"])]:
        dy = -1*PLAYER_SPEED
        current_direction = "UP"
        is_moving = True
    elif keys[pygame.key.key_code(Settings_options["MOVE DOWN:"])]:
        dy = 1*PLAYER_SPEED
        current_direction = "DOWN"
        is_moving = True
    elif keys[pygame.key.key_code(Settings_options["MOVE LEFT:"])]:
        dx = -1*PLAYER_SPEED
        current_direction= "LEFT"
        is_moving = True
    elif keys[pygame.key.key_code(Settings_options["MOVE RIGHT:"])]:
        dx = 1*PLAYER_SPEED
        current_direction= "RIGHT"
        is_moving = True
    else:
        is_moving = False
    # Update player position based on movement
    new_x = player_position[0] + dx
    new_y = player_position[1] + dy

    #BLOCK COLISSIONS
    for row in blocks_positions:
        for block_x, block_y in row:
            # Check if the player collides with any block
            if (new_x + PLAYER_SIZE> block_x and new_x < block_x + BLOCK_SIZE and
                    new_y + PLAYER_SIZE > block_y and new_y < block_y + BLOCK_SIZE):
                # If there's a collision, don't update the player position
                return player_position, "level_1", is_moving, current_direction


    # Ensure new position is within boundaries
    if  240 <= new_x and  new_x <= HWIDTH - BLOCK_SIZE and 60 <= new_y and new_y <= HHEIGHT - BLOCK_SIZE:
        player_position = (new_x, new_y)

    return player_position, "level_1", is_moving, current_direction
