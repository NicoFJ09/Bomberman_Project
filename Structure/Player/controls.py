import pygame
from var_consts import *
import time

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
def handle_bomb_explosion(screen, bombs_list, typeobject, player_position, player_lives, Dblock):
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

        # Horizontal explosion rectangle
        explosion_rect_horizontal = pygame.Rect(bomb_x - BLOCK_SIZE, bomb_y, 3 * BLOCK_SIZE, BLOCK_SIZE)

        # Vertical explosion rectangle
        explosion_rect_vertical = pygame.Rect(bomb_x, bomb_y - BLOCK_SIZE, BLOCK_SIZE, 3 * BLOCK_SIZE)

        # Check if the bomb has exploded
        if not Bomb_explode:
            if player_lives > 0 and (player_rect.colliderect(explosion_rect_horizontal) or player_rect.colliderect(explosion_rect_vertical)):
                # If there's a collision with bomb explosion, decrement player lives
                player_lives -= 1
                # Set the bomb as exploded
                Bomb_explode = True
                # If player has no lives left, handle game over condition
                if player_lives <= 0:
                    # Handle game over condition here
                    return player_lives, Dblock
            # Iterate over the blocks in Dblock and check for collision with explosion
            # Remove collided blocks from Dblock
            remove_collided_blocks(explosion_rect_horizontal, Dblock)
            remove_collided_blocks(explosion_rect_vertical, Dblock)
            Bomb_explode = True
            return player_lives, Dblock
                
        # Delay before clearing the bombs list
        if current_time >= bomb_explosion_time + EXPLOSION_DURATION_SECONDS:
            bombs_list.clear()  # Clear the bombs list after the explosion effect duration
            Bomb_explode = False  # Reset Bomb_exploded back to False
        return player_lives, Dblock
    
    return player_lives, Dblock

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
    
    if not detect_explosion_collision(explosion_rect):
        pygame.draw.rect(screen, (255, 0, 0), explosion_rect)

    draw_explosion_horizontal(screen, bomb_x, bomb_y, offset + BLOCK_SIZE, typeobject)

def draw_explosion_vertical(screen, bomb_x, bomb_y, offset,typeobject):
    # Base case: if offset exceeds the explosion range, stop drawing vertically
    if abs(offset) > BLOCK_SIZE:
        return

    # Draw the explosion block vertically
    explosion_rect = pygame.Rect(bomb_x + BLOCK_SIZE // 4, bomb_y + offset, BLOCK_SIZE // 2, BLOCK_SIZE)
    
    if not detect_explosion_collision(explosion_rect):
        pygame.draw.rect(screen, (255, 0, 0), explosion_rect)
    
    draw_explosion_vertical(screen, bomb_x, bomb_y, offset + BLOCK_SIZE, typeobject )

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

def remove_collided_blocks(explosion_rect, Dblock):
    # Helper function to recursively remove collided blocks
    def remove_blocks_recursive(block_list, index=0):
        # Base case: if the index exceeds the length of the block list, return
        if index >= len(block_list):
            return

        # Get the current block position
        block_position = block_list[index]
        block_rect = pygame.Rect(block_position[0], block_position[1], BLOCK_SIZE, BLOCK_SIZE)

        # If the block collides with the explosion rectangle, remove it
        if block_rect.colliderect(explosion_rect):
            if block_position in block_list:
                block_list.remove(block_position)
            # Adjust the index after removing the block
            index -= 1

        # Move to the next block position by making a recursive call with the updated index
        remove_blocks_recursive(block_list, index + 1)

    # Helper function to apply remove_blocks_recursive to each block list in Dblock
    def apply_to_dblock(block_index=0):
        if block_index >= len(Dblock):
            return
        remove_blocks_recursive(Dblock[block_index])
        apply_to_dblock(block_index + 1)

    # Start the recursion by passing the first block list in Dblock
    apply_to_dblock()



#========================================= BLOCK DESTRUCTION  ====================================