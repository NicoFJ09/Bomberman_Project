import pygame
from var_consts import *
import time
def handle_player_actions(Settings_options, current_screen, player_position, is_moving, current_direction, blocks_positions, bombs_list, enemy_rect, enemy_rect2, enemy_rect3):
    global bombs, lives
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
    if bombs > 0 and keys[pygame.key.key_code(Settings_options["DROP BOMB:"])] and not bombs_list:
        bombs_list.append(((round(player_position[0] / BLOCK_SIZE) * BLOCK_SIZE, round(player_position[1] / BLOCK_SIZE) * BLOCK_SIZE)))
        bombs -= 1
        print("Bombs left:", bombs)
        global bomb_explosion_time
        bomb_explosion_time = time.time()


    # Update player position based on movement
    new_x = player_position[0] + dx
    new_y = player_position[1] + dy

    # Check for collisions recursively
    player_position, is_moving, current_direction = check_collision(
        blocks_positions, new_x, new_y, player_position, is_moving, current_direction
    )
    player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
    if player_rect.colliderect(enemy_rect) or player_rect.colliderect(enemy_rect2) or player_rect.colliderect(enemy_rect3):
        lives -= 1
        print(lives)
    update_enemy_position(enemy_rect, player_position, 240, HWIDTH - BLOCK_SIZE - ENEMY_SIZE, is_moving)
    update_enemy_position(enemy_rect2, player_position, min_distance, max_distance, is_moving)
    update_enemy_position(enemy_rect3, player_position, min_distance, max_distance, is_moving)
    return player_position, current_screen, current_screen, current_screen, is_moving, current_direction, bombs



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
def handle_bomb_explosion(screen, bombs_list, typeobject, player_position, player_lives):
    global bomb_explosion_time, Bomb_explode
    
    # Get the current time
    current_time = time.time()
    
    # Check if there is a bomb and if its explosion time has passed
    if bombs_list and current_time >= bomb_explosion_time + BOMB_DURATION_SECONDS:
        # Get the bomb position
        bomb_x, bomb_y = bombs_list[0]
        
        # Draw explosion effect
        draw_explosion(screen, bomb_x, bomb_y, typeobject)
        
        # Check collision between player and bomb explosion
        player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
        explosion_rect = pygame.Rect(bomb_x - BLOCK_SIZE, bomb_y - BLOCK_SIZE, 3 * BLOCK_SIZE, 3 * BLOCK_SIZE)
        # Check if the bomb has exploded
        if not Bomb_explode:
            if player_lives > 0 and player_rect.colliderect(explosion_rect):
                # If there's a collision with bomb explosion, decrement player lives
                player_lives -= 1
                # Set the bomb as exploded
                Bomb_explode = True
                # If player has no lives left, handle game over condition
                if player_lives <= 0:
                    # Handle game over condition here
                    return player_lives
        
        # Delay before clearing the bombs list
        if current_time >= bomb_explosion_time + EXPLOSION_DURATION_SECONDS:
            bombs_list.clear()  # Clear the bombs list after the explosion effect duration
            Bomb_explode = False  # Reset Bomb_exploded back to False
        print(player_lives)
        return player_lives
    
    return player_lives

def draw_explosion(screen, bomb_x, bomb_y, typeobject):
    # Draw explosion effect (red blocks in all directions)
    explosion_range = BLOCK_SIZE-1  # The range of the explosion
    
    # Draw explosion horizontally
    draw_explosion_horizontal(screen, bomb_x, bomb_y, -explosion_range, typeobject)
    draw_explosion_horizontal(screen, bomb_x, bomb_y, explosion_range, typeobject)
    
    # Draw explosion vertically
    draw_explosion_vertical(screen, bomb_x, bomb_y, -explosion_range, typeobject)
    draw_explosion_vertical(screen, bomb_x, bomb_y, explosion_range, typeobject)

def draw_explosion_horizontal(screen, bomb_x, bomb_y, offset, typeobject):
    # Base case: if offset exceeds the explosion range, stop drawing horizontally
    if abs(offset) > BLOCK_SIZE:
        return
    
    # Draw the explosion block horizontally
    explosion_rect = pygame.Rect(bomb_x + offset, bomb_y + BLOCK_SIZE // 4, BLOCK_SIZE, BLOCK_SIZE // 2)
    
    if not detect_explosion_collision(explosion_rect,typeobject):
        pygame.draw.rect(screen, (255, 0, 0), explosion_rect)

    draw_explosion_horizontal(screen, bomb_x, bomb_y, offset + BLOCK_SIZE, typeobject)

def draw_explosion_vertical(screen, bomb_x, bomb_y, offset,typeobject):
    # Base case: if offset exceeds the explosion range, stop drawing vertically
    if abs(offset) > BLOCK_SIZE:
        return

    # Draw the explosion block vertically
    explosion_rect = pygame.Rect(bomb_x + BLOCK_SIZE // 4, bomb_y + offset, BLOCK_SIZE // 2, BLOCK_SIZE)
    
    if not detect_explosion_collision(explosion_rect,typeobject):
        pygame.draw.rect(screen, (255, 0, 0), explosion_rect)
    
    draw_explosion_vertical(screen, bomb_x, bomb_y, offset + BLOCK_SIZE, typeobject )

def detect_explosion_collision(explosion_rect, typeobject):
    for i, block in enumerate(typeobject):
        for block_x, block_y in block:
            block_rect = pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
            if explosion_rect.colliderect(block_rect):
                # Check if the typeobject has less than 12 indexes
                if len(typeobject) <= 12:
                    # Delete the block from the typeobject
                    del typeobject[i]
                return True  # Collision detected with a block
    return False  # No collision detected with any block



#========================================= ENEMY SPAWN  ====================================

# Function to create enemy rectangle
def create_enemy(x, y):
    return pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)

# Function to draw enemies
def draw_enemies(screen, enemy_rect, enemy_image):
    screen.blit(enemy_image, enemy_rect)
def update_enemy_position(enemy_rect, player_position, min_distance, max_distance, is_player_moving):
    global ENEMY_SPEED, enemy_direction

    # Check if the player is moving
    if is_player_moving:
        # Check the relative position of the player and the enemy
        if enemy_rect.x < player_position[0]:
            enemy_direction = 'right'
        elif enemy_rect.x > player_position[0]:
            enemy_direction = 'left'

        # Move the enemy based on its current direction
        if enemy_direction == 'right':
            enemy_rect.x += ENEMY_SPEED * ENEMY_SIZE
            # Check if the enemy has reached the maximum distance
            if enemy_rect.x > max_distance:
                enemy_rect.x = max_distance
        elif enemy_direction == 'left':
            enemy_rect.x -= ENEMY_SPEED * ENEMY_SIZE
            # Check if the enemy has reached the minimum distance
            if enemy_rect.x < min_distance:
                enemy_rect.x = min_distance
    return enemy_rect
