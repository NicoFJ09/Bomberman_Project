import pygame
from var_consts import *
def handle_player_actions(Settings_options, player_position, is_moving, current_direction, blocks_positions, bombs_list):
    # By default, no movement
    dx, dy = 0, 0

    # Check if any movement keys are held down
    keys = pygame.key.get_pressed()

    if keys[pygame.key.key_code(Settings_options["PAUSE:"])]:
        return player_position, "PAUSED", False, current_direction
    elif keys[pygame.key.key_code(Settings_options["RESTART:"])]:
        return [240,60], "RESTART (A LIFE WILL BE LOST)", False, "RIGHT"

    # Handle movement keys
    if keys[pygame.key.key_code(Settings_options["MOVE UP:"])]:
        dy = -1 * PLAYER_SPEED
        current_direction = "UP"
        is_moving = True
    elif keys[pygame.key.key_code(Settings_options["MOVE DOWN:"])]:
        dy = 1 * PLAYER_SPEED
        current_direction = "DOWN"
        is_moving = True
    elif keys[pygame.key.key_code(Settings_options["MOVE LEFT:"])]:
        dx = -1 * PLAYER_SPEED
        current_direction = "LEFT"
        is_moving = True
    elif keys[pygame.key.key_code(Settings_options["MOVE RIGHT:"])]:
        dx = 1 * PLAYER_SPEED
        current_direction = "RIGHT"
        is_moving = True
    else:
        is_moving = False
    # Handle bomb placement
    if keys[pygame.key.key_code(Settings_options["DROP BOMB:"])]:
        if not bombs_list:
            # Adjust bomb placement based on current direction
            if current_direction == "UP":
                bombs_list.append((player_position[0], player_position[1] + (BLOCK_SIZE-15)))
            elif current_direction == "DOWN":
                bombs_list.append((player_position[0], player_position[1] - (BLOCK_SIZE-15)))
            elif current_direction == "LEFT":
                bombs_list.append((player_position[0] + (BLOCK_SIZE-15), player_position[1]))
            elif current_direction == "RIGHT":
                bombs_list.append((player_position[0] - (BLOCK_SIZE-15), player_position[1]))

    
    # Update player position based on movement
    new_x = player_position[0] + dx
    new_y = player_position[1] + dy

    # Check for collisions recursively
    player_position, _, is_moving, current_direction = check_collision(
        blocks_positions, new_x, new_y, player_position, is_moving, current_direction
    )

    return player_position, "level_1", is_moving, current_direction



#============================== COLLISIONS CONTROL==============================


def check_collision(blocks_positions, new_x, new_y, player_position, is_moving, current_direction, index=0, inner_index=0):
    # Base case: check if we've reached the end of the blocks_positions list
    if index >= len(blocks_positions):
        # Ensure new position is within boundaries if there are no collisions
        if 240 <= new_x <= HWIDTH - BLOCK_SIZE and 60 <= new_y <= HHEIGHT - BLOCK_SIZE:
            player_position = (new_x, new_y)
        return player_position, "level_1", is_moving, current_direction

    # Calculate the center of the player sprite
    player_center_x = new_x + BLOCK_SIZE // 2
    player_center_y = new_y + BLOCK_SIZE // 2

    # Calculate the offset for the hitbox from the center of the sprite
    hitbox_offset = (BLOCK_SIZE - PLAYER_SIZE) // 2

    # Get the current block's coordinates
    block_x, block_y = blocks_positions[index][inner_index]

    # Calculate the bounds of the block
    block_left = block_x
    block_right = block_x + BLOCK_SIZE
    block_top = block_y
    block_bottom = block_y + BLOCK_SIZE

    # Check for collision between player and block hitbox
    if (player_center_x + hitbox_offset > block_left and player_center_x - hitbox_offset < block_right and
            player_center_y + hitbox_offset > block_top and player_center_y - hitbox_offset < block_bottom):
        # If there's a collision, don't update the player position
        return player_position, "level_1", is_moving, current_direction

    # Check for collision with the bomb if bombs exist
    if bombs_list:
        bomb_center_x = bombs_list[0][0] + BLOCK_SIZE // 2
        bomb_center_y = bombs_list[0][1] + BLOCK_SIZE // 2
        if (player_center_x + hitbox_offset > bombs_list[0][0] and player_center_x - hitbox_offset < bombs_list[0][0] + BLOCK_SIZE and
                player_center_y + hitbox_offset > bombs_list[0][1] and player_center_y - hitbox_offset < bombs_list[0][1] + BLOCK_SIZE):
            # If there's a collision with the bomb, don't update the player position
            return player_position, "level_1", is_moving, current_direction


    # Move to the next block
    inner_index += 1
    if inner_index >= len(blocks_positions[index]):
        inner_index = 0
        index += 1

    # Recursively call the function with updated indices
    return check_collision(blocks_positions, new_x, new_y, player_position, is_moving, current_direction, index, inner_index)

