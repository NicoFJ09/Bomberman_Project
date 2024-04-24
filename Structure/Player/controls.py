import pygame
from var_consts import *
import time
def handle_player_actions(Settings_options, current_screen, player_position, is_moving, current_direction, blocks_positions, bombs_list,screen):
    global bomb_explosion_time
    # By default, no movement
    dx, dy = 0, 0

    # Check if any movement keys are held down
    keys = pygame.key.get_pressed()

    if keys[pygame.key.key_code(Settings_options["PAUSE:"])]:
        return player_position, "PAUSED", "paused", current_screen, False, current_direction
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
                bombs_list.append(((round(player_position[0]/BLOCK_SIZE)*BLOCK_SIZE , (round(player_position[1]/BLOCK_SIZE))*BLOCK_SIZE)))
                print((((round(player_position[0]/BLOCK_SIZE)*BLOCK_SIZE) , (round(player_position[1]/BLOCK_SIZE))*BLOCK_SIZE)))
            # Set bomb explosion time
                global bomb_explosion_time
                bomb_explosion_time = time.time()
        return player_position, current_screen, current_screen, current_screen,is_moving, current_direction




    # Update player position based on movement
    new_x = player_position[0] + dx
    new_y = player_position[1] + dy

    # Check for collisions recursively
    player_position, is_moving, current_direction = check_collision(
        blocks_positions, new_x, new_y, player_position, is_moving, current_direction
    )

    return player_position, current_screen, current_screen, current_screen, is_moving, current_direction



#============================== COLLISIONS CONTROL==============================


def check_collision(blocks_positions, new_x, new_y, player_position, is_moving, current_direction, index=0, inner_index=0):
    # Base case: check if we've reached the end of the blocks_positions list
    if index >= len(blocks_positions):
        # Ensure new position is within boundaries if there are no collisions
        if 240 <= new_x <= HWIDTH - BLOCK_SIZE and 60 <= new_y <= HHEIGHT - BLOCK_SIZE:
            player_position = (new_x, new_y)
        return player_position, is_moving, current_direction

    # Create a Rect object for the player's position and hitbox
    player_rect = pygame.Rect(new_x + (BLOCK_SIZE - PLAYER_SIZE) // 2, new_y + (BLOCK_SIZE - PLAYER_SIZE) // 2, PLAYER_SIZE, PLAYER_SIZE)
    # Get the current block's coordinates
    block_x, block_y = blocks_positions[index][inner_index]
    
    # Create a Rect object for the current block
    block_rect = pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)

    # Check for collision between player and block hitbox
    if player_rect.colliderect(block_rect):
        # If there's a collision, don't update the player position
        return player_position, is_moving, current_direction

    # Move to the next block
    inner_index += 1
    if inner_index >= len(blocks_positions[index]):
        inner_index = 0
        index += 1

    # Recursively call the function with updated indices
    return check_collision(blocks_positions, new_x, new_y, player_position, is_moving, current_direction, index, inner_index)
#=============================== BOMB EXPLOSION ====================================
def handle_bomb_explosion(screen, bombs_list):
    global bomb_explosion_time
    
    # Get the current time
    current_time = time.time()
    
    # Check if there is a bomb and if its explosion time has passed
    if bombs_list and current_time >= bomb_explosion_time + BOMB_DURATION_SECONDS:
        # Get the bomb position
        bomb_x, bomb_y = bombs_list[0]
        
        # Draw explosion effect
        draw_explosion(screen, bomb_x, bomb_y)
        
        # Delay before clearing the bombs list
        if current_time >= bomb_explosion_time + EXPLOSION_DURATION_SECONDS:
            bombs_list.clear()  # Clear the bombs list after the explosion effect duration
            
        return True  # Indicate that the bomb has exploded

    return False


def draw_explosion(screen, bomb_x, bomb_y):
    # Draw explosion effect (red blocks in all directions)
    explosion_range = BLOCK_SIZE-1  # The range of the explosion
    
    # Draw explosion horizontally
    draw_explosion_horizontal(screen, bomb_x, bomb_y, -explosion_range)
    draw_explosion_horizontal(screen, bomb_x, bomb_y, explosion_range)
    
    # Draw explosion vertically
    draw_explosion_vertical(screen, bomb_x, bomb_y, -explosion_range)
    draw_explosion_vertical(screen, bomb_x, bomb_y, explosion_range)

def draw_explosion_horizontal(screen, bomb_x, bomb_y, offset):
    # Base case: if offset exceeds the explosion range, stop drawing horizontally
    if abs(offset) > BLOCK_SIZE:
        return
    
    # Draw the explosion block horizontally
    explosion_rect = pygame.Rect(bomb_x + offset, bomb_y + BLOCK_SIZE // 4, BLOCK_SIZE, BLOCK_SIZE // 2)
    
    if not detect_explosion_collision(explosion_rect):
        pygame.draw.rect(screen, (255, 0, 0), explosion_rect)

    draw_explosion_horizontal(screen, bomb_x, bomb_y, offset + BLOCK_SIZE)

def draw_explosion_vertical(screen, bomb_x, bomb_y, offset):
    # Base case: if offset exceeds the explosion range, stop drawing vertically
    if abs(offset) > BLOCK_SIZE:
        return

    # Draw the explosion block vertically
    explosion_rect = pygame.Rect(bomb_x + BLOCK_SIZE // 4, bomb_y + offset, BLOCK_SIZE // 2, BLOCK_SIZE)
    
    if not detect_explosion_collision(explosion_rect):
        pygame.draw.rect(screen, (255, 0, 0), explosion_rect)
    
    draw_explosion_vertical(screen, bomb_x, bomb_y, offset + BLOCK_SIZE)

def detect_explosion_collision(explosion_rect):
    for block in blocks_positions:
        for block_x, block_y in block:
            block_rect = pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
            if explosion_rect.colliderect(block_rect):
                return True  # Collision detected with a block
    return False  # No collision detected with any block

