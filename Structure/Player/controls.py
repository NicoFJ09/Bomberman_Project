import pygame
from var_consts import *
import time
import random
#=====================================================PLAYER CONTROL AND ENTITIES COLISSION MANAGEMENT=================================================================

def handle_player_actions(Settings_options, current_screen, player_position, is_moving, current_direction, blocks_positions, bombs_list, bombs):
    # By default, no movement
    dx, dy = 0, 0

    # Check if any movement keys are held down
    keys = pygame.key.get_pressed()

    if keys[pygame.key.key_code(Settings_options["PAUSE:"])]:
        return player_position, "PAUSED", "paused", current_screen, False, current_direction, bombs

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
        global bomb_explosion_time
        bomb_explosion_time = time.time()


    # Update player position based on movement
    new_x = player_position[0] + dx
    new_y = player_position[1] + dy

    # Check for collisions recursively
    player_position, is_moving, current_direction = check_collision(
        blocks_positions, new_x, new_y, player_position, is_moving, current_direction
    )

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
def handle_bomb_explosion(screen, bombs_list, explosion_sprite_sheet, player_position, player_lives, Dblock, points, enemy_position):
    global bomb_explosion_time, Bomb_explode

    # Get the current time
    current_time = time.time()

    # Check if there is a bomb and if its explosion time has passed
    if bombs_list and current_time >= bomb_explosion_time + BOMB_DURATION_SECONDS:
        # Get the bomb position
        bomb_x, bomb_y = bombs_list[0]

        # Draw explosion effect
        draw_explosion(screen, bomb_x, bomb_y, explosion_sprite_sheet)

        # Check collision between player and bomb explosion
        player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)

        # Horizontal explosion rectangle
        explosion_rect_horizontal = pygame.Rect(bomb_x - BLOCK_SIZE, bomb_y, 3 * BLOCK_SIZE, BLOCK_SIZE)

        # Vertical explosion rectangle
        explosion_rect_vertical = pygame.Rect(bomb_x, bomb_y - BLOCK_SIZE, BLOCK_SIZE, 3 * BLOCK_SIZE)

        enemy_rect = pygame.Rect(enemy_position["x"], enemy_position["y"], ENEMY_SIZE, ENEMY_SIZE)
        # Flag to track if player is hit by explosion
        player_hit = False
        enemy_hit = False

        # Check if the bomb has exploded
        if not Bomb_explode:

            # Remove collided blocks
            points = remove_collided_blocks(explosion_rect_horizontal, Dblock, points)
            points = remove_collided_blocks(explosion_rect_vertical, Dblock, points)
            
            # Check for player collision with bomb explosion
            if player_lives > 0 and (player_rect.colliderect(explosion_rect_horizontal) or player_rect.colliderect(explosion_rect_vertical)):
                # If there's a collision with bomb explosion, decrement player lives
                player_lives -= 1
                player_hit = True  # Set flag to True
                Bomb_explode= True
            if enemy_rect.colliderect(explosion_rect_horizontal) or enemy_rect.colliderect(explosion_rect_vertical):
                direction = enemy_position["direction"]
                enemy_position = {"x": -2*ENEMY_SIZE, "y": -2*ENEMY_SIZE, "direction": direction}
                points += 1000
                enemy_hit = True
                Bomb_explode= True

        # Delay before clearing the bombs list
        if current_time >= bomb_explosion_time + EXPLOSION_DURATION_SECONDS:
            bombs_list.clear()  # Clear the bombs list after the explosion effect duration
            Bomb_explode = False  # Reset Bomb_exploded back to False

        # If player or enemy is hit by explosion, return immediately
        if player_hit or enemy_hit:
            return player_lives, Dblock, points, enemy_position

    # Add a default return statement
    return player_lives, Dblock, points, enemy_position

def draw_explosion(screen, bomb_x, bomb_y, explosion_sprite_sheet):
    # Draw explosion effect (red blocks in all directions)
    explosion_range = BLOCK_SIZE-1  # The range of the explosion
    
    # Draw explosion horizontally
    draw_explosion_horizontal(screen, bomb_x, bomb_y, -explosion_range, explosion_sprite_sheet)
    draw_explosion_horizontal(screen, bomb_x, bomb_y, explosion_range, explosion_sprite_sheet)
    
    # Draw explosion vertically
    draw_explosion_vertical(screen, bomb_x, bomb_y, -explosion_range, explosion_sprite_sheet)
    draw_explosion_vertical(screen, bomb_x, bomb_y, explosion_range, explosion_sprite_sheet)

def draw_explosion_horizontal(screen, bomb_x, bomb_y, offset, explosion_image):
    # Base case: if offset exceeds the explosion range, stop drawing horizontally
    if abs(offset) > BLOCK_SIZE:
        return
    
    # Calculate the position of the explosion block
    explosion_rect = pygame.Rect(bomb_x + offset, bomb_y + BLOCK_SIZE // 4, BLOCK_SIZE, BLOCK_SIZE // 2)
    
    # Check if the explosion block collides with any objects
    if not detect_explosion_collision(explosion_rect):
        # Draw the explosion block
        stored_explosion_rect = explosion_rect.copy()
        stored_explosion_rect.y -= 15
        screen.blit(explosion_image, stored_explosion_rect)
    
    draw_explosion_horizontal(screen, bomb_x, bomb_y, offset + BLOCK_SIZE, explosion_image)


def draw_explosion_vertical(screen, bomb_x, bomb_y, offset, explosion_image):
    # Base case: if offset exceeds the explosion range, stop drawing vertically
    if abs(offset) > BLOCK_SIZE:
        return
    
    # Calculate the position of the explosion block
    explosion_rect = pygame.Rect(bomb_x + BLOCK_SIZE // 4, bomb_y + offset, BLOCK_SIZE // 2, BLOCK_SIZE)
    
    # Check if the explosion block collides with any objects
    if not detect_explosion_collision(explosion_rect):
        # Draw the explosion block
        stored_explosion_rect = explosion_rect.copy()
        stored_explosion_rect.x -= 15
        screen.blit(explosion_image, stored_explosion_rect)
    
    draw_explosion_vertical(screen, bomb_x, bomb_y, offset + BLOCK_SIZE, explosion_image)


def detect_explosion_collision_aux(explosion_rect, row_index=0, col_index=0):
    # Base case: if all rows have been checked
    if row_index >= len(blocks_positions):
        return False  # No collision detected with any block
    
    # Base case: if all columns within the current row have been checked
    if col_index >= len(blocks_positions[row_index]):
        # Move to the next row
        return detect_explosion_collision_aux(explosion_rect, row_index + 1, 0)
    
    # Extract the block position
    block_x, block_y = blocks_positions[row_index][col_index]
    
    # Create the block rectangle
    block_rect = pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
    
    # Check collision
    if explosion_rect.colliderect(block_rect):
        return True  # Collision detected with a block
    else:
        # Recursive call to check the next column within the current row
        return detect_explosion_collision_aux(explosion_rect, row_index, col_index + 1)

# Wrapper function to start the recursion
def detect_explosion_collision(explosion_rect):
    return detect_explosion_collision_aux(explosion_rect)

#========================================= BLOCK DESTRUCTION  ====================================

def remove_collided_blocks(explosion_rect, Dblock, points):
    
    # Helper function to recursively remove collided blocks
    def remove_blocks_recursive(block_list, points, index=0):
        global Bomb_explode
        # Base case: if the index exceeds the length of the block list, return
        if index >= len(block_list):
            return points

        # Get the current block position
        block_position = block_list[index]
        block_rect = pygame.Rect(block_position[0], block_position[1], BLOCK_SIZE, BLOCK_SIZE)

        # If the block collides with the explosion rectangle, remove it
        if block_rect.colliderect(explosion_rect):
            if block_position in block_list:
                block_list.remove(block_position)
                points += 500
            # Adjust the index after removing the block
            index -= 1
            

        # Move to the next block position by making a recursive call with the updated index
        return remove_blocks_recursive(block_list, points, index + 1)

    # Helper function to apply remove_blocks_recursive to each block list in Dblock
    def apply_to_dblock(points, block_index=0):
        if block_index >= len(Dblock):
            return points
        points = remove_blocks_recursive(Dblock[block_index], points)
        return apply_to_dblock(points, block_index + 1)

    # Start the recursion by passing the first block list in Dblock
    return apply_to_dblock(points)

#========================================================= ENEMY MOVEMENT AND LOGIC ============================================================

def create_enemy(spawn_positions):
    # Create a new enemy with a predefined spawn position and random direction
    x, y = spawn_positions
    direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
    return {"x": x, "y": y, "direction": direction}

def move_enemy(enemy):
    # Move enemy based on current direction
    if enemy["direction"] == "LEFT":
        enemy["x"] -= ENEMY_SPEED
    elif enemy["direction"] == "RIGHT":
        enemy["x"] += ENEMY_SPEED
    elif enemy["direction"] == "UP":
        enemy["y"] -= ENEMY_SPEED
    elif enemy["direction"] == "DOWN":
        enemy["y"] += ENEMY_SPEED
    return enemy

def check_enemy_collision(blocks_positions, enemy):
    global collision_count  # Access the global collision count variable

    def check_collision_recursive(block_groups, block_group_index):
        if block_group_index >= len(block_groups):
            return False
        else:
            block_group = block_groups[block_group_index]
            return check_blocks_in_group(block_group, 0) or check_collision_recursive(block_groups, block_group_index + 1)

    def check_blocks_in_group(block_group, block_index):
        if block_index >= len(block_group):
            return False
        else:
            block_x, block_y = block_group[block_index]
            block_rect = pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
            enemy_rect = pygame.Rect(enemy["x"] + 10, enemy["y"] + 10, ENEMY_SIZE - 20, ENEMY_SIZE - 20)
            if enemy_rect.colliderect(block_rect):
                global collision_count
                collision_count += 1
                if enemy["direction"] == "LEFT":
                    enemy["x"] += 15
                elif enemy["direction"] == "RIGHT":
                    enemy["x"] -= 15
                elif enemy["direction"] == "UP":
                    enemy["y"] += 15
                elif enemy["direction"] == "DOWN":
                    enemy["y"] -= 15
                return True
            else:
                return check_blocks_in_group(block_group, block_index + 1)

    collision_detected = check_collision_recursive(blocks_positions, 0)

    if collision_detected:
        if enemy["direction"] in ["LEFT", "RIGHT"]:
            enemy["direction"] = random.choice(["UP", "DOWN"])
        else:
            enemy["direction"] = random.choice(["LEFT", "RIGHT"])
        collision_count = 0

    enemy = move_enemy(enemy)

    return enemy


def create_secondary_enemy(spawn_positions):
    # Create a new enemy with a predefined spawn position and random direction
    x, y = spawn_positions
    direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
    return {"x": x, "y": y, "direction": direction}

def move_secondary_enemy(enemy):
    # Move enemy based on current direction
    if enemy["direction"] == "LEFT" or enemy["direction"] == "RIGHT":
        enemy["x"] += ENEMY_SPEED if enemy["direction"] == "RIGHT" else -ENEMY_SPEED
    elif enemy["direction"] == "UP" or enemy["direction"] == "DOWN":
        enemy["y"] += ENEMY_SPEED if enemy["direction"] == "DOWN" else -ENEMY_SPEED
    return enemy

def check_secondary_enemy_collision(blocks_positions, enemy):
    global collision_count  # Access the global collision count variable

    def check_collision_recursive(block_groups, index):
        if index >= len(block_groups):
            return False  # No collision detected in any block group
        else:
            block_group = block_groups[index]
            collision_detected = check_blocks_in_group(block_group, 0)
            if collision_detected:
                return True  # Collision detected in this block group
            else:
                return check_collision_recursive(block_groups, index + 1)

    def check_blocks_in_group(block_group, index):
        if index >= len(block_group):
            return False  # No collision detected in this block group
        else:
            block_x, block_y = block_group[index]
            # Increase the enemy hitbox by reducing the dimensions of the enemy's rectangle
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], ENEMY_SIZE, ENEMY_SIZE)
            block_rect = pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
            if enemy_rect.colliderect(block_rect):
                global collision_count
                # Move the enemy back by a few pixels
                if enemy["direction"] == "LEFT" or enemy["direction"] == "RIGHT":
                    enemy["x"] -= 5 if enemy["direction"] == "RIGHT" else -5
                elif enemy["direction"] == "UP" or enemy["direction"] == "DOWN":
                    enemy["y"] -= 5 if enemy["direction"] == "DOWN" else -5
                # Change direction
                enemy["direction"] = random.choice(["LEFT", "RIGHT"]) if enemy["direction"] in ["LEFT", "RIGHT"] else random.choice(["UP", "DOWN"])
                return True  # Collision detected with this block
            else:
                return check_blocks_in_group(block_group, index + 1)

    collision_detected = check_collision_recursive(blocks_positions, 0)
    
    # Move the enemy only if no collision was detected
    if not collision_detected:
        enemy = move_secondary_enemy(enemy)

    return enemy

# Define a constant for the cooldown duration in seconds
COOLDOWN_DURATION = 1.0  # Adjust the duration as needed

# Define a variable to store the time of the last collision
last_collision_time = 0.0

def handle_enemy_collision(player_position, enemy, enemy_size, player_lives, collision_state=False):
    global last_collision_time
    
    # Get the current time
    current_time = time.time()
    
    # Check if enough time has passed since the last collision
    if current_time - last_collision_time >= COOLDOWN_DURATION:
        # Unpack the enemy dictionary into x and y coordinates
        enemy_x, enemy_y = enemy["x"], enemy["y"]

        # Create Rect objects for the player's position and hitbox
        player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
        # Create a Rect object for the enemy's position and hitbox
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

        # Check for collision between player and enemy
        if player_rect.colliderect(enemy_rect):
            # If the player is colliding with the enemy and was not previously colliding, decrement player lives
            if not collision_state:
                player_lives -= 1
                # Set collision state to True to indicate the player is currently colliding
                collision_state = True
                # Update the last collision time
                last_collision_time = current_time
                # Return immediately after decrementing lives
                return player_lives, collision_state
    
    # If the player is not colliding with the enemy and was previously colliding, reset collision state
    if collision_state:
        collision_state = False
    
    return player_lives, collision_state