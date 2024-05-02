import pygame
from var_consts import *
import time
def extract_frames(sprite_sheet_image, num_frames_per_direction, frame_width, frame_height, frames=None, i=0):
    # Initialize frames list on the first call
    if frames is None:
        frames = []

    # Base case: if we have extracted the desired number of frames, return
    if i >= num_frames_per_direction:
        return frames

    # Extract frame and append it to the frames list
    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
    frame_image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
    frame_image.blit(sprite_sheet_image, (0, 0), frame_rect)
    frames.append(frame_image)

    # Recursive call to extract the next frame
    return extract_frames(sprite_sheet_image, num_frames_per_direction, frame_width, frame_height, frames, i+1)


def draw_player(screen, player_position, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite,current_direction, is_moving, frame_counter):
    if selected_skin_option == "Bomberman":
        if current_direction == "UP":
            frames = extract_frames(B_up_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "DOWN":
            frames = extract_frames(B_down_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "LEFT":
            frames = extract_frames(B_left_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "RIGHT":
            frames = extract_frames(B_right_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        else:
            frames = []  # Ensure frames is assigned a value in all cases
        if is_moving:
            screen.blit(frames[(frame_counter // FRAME_DURATION) % num_frames_per_direction], player_position)
        else:
            screen.blit(frames[0], player_position)  # Draw idle frame

    elif selected_skin_option == "Kirby":
        if current_direction == "UP":
            frames = extract_frames(K_up_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "DOWN":
            frames = extract_frames(K_down_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "LEFT":
            frames = extract_frames(K_left_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "RIGHT":
            frames = extract_frames(K_right_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        else:
            frames = []  # Ensure frames is assigned a value in all cases
        if is_moving:
            screen.blit(frames[(frame_counter // FRAME_DURATION) % num_frames_per_direction], player_position)
        else:
            screen.blit(frames[0], player_position)  # Draw idle frame

    elif selected_skin_option == "Samus":
        if current_direction == "UP":
            frames = extract_frames(S_left_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "DOWN":
            frames = extract_frames(S_right_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "LEFT":
            frames = extract_frames(S_left_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "RIGHT":
            frames = extract_frames(S_right_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        else:
            frames = []  # Ensure frames is assigned a value in all cases
        if is_moving:
            screen.blit(frames[(frame_counter // FRAME_DURATION) % num_frames_per_direction], player_position)
        else:
            screen.blit(frames[0], player_position)  # Draw idle frame



def draw_blocks(screen, BLOCK_SPRITE, typeobject, index=0):
    # Base case: check if we've reached the end of the typeobject list
    if index >= len(typeobject):
        return
    
    # Draw the current row
    draw_row(screen, BLOCK_SPRITE, typeobject[index])
    
    # Recursively call the function with updated index
    draw_blocks(screen, BLOCK_SPRITE, typeobject, index + 1)

def draw_row(screen, BLOCK_SPRITE, row, inner_index=0):
    # Base case: check if we've reached the end of the row
    if inner_index >= len(row):
        return
    
    # Draw the current block
    x, y = row[inner_index]
    block_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    screen.blit(BLOCK_SPRITE, block_rect)
    
    # Recursively call the function with updated inner_index
    draw_row(screen, BLOCK_SPRITE, row, inner_index + 1)


def draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter):
    # Check if there are any bombs in the list
    bomb_sprite = None
    if selected_skin_option == "Bomberman":
        bomb_sprite = extract_frames(Bbomb_load_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
    elif selected_skin_option == "Kirby":
        bomb_sprite = extract_frames(Kbomb_load_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
    elif selected_skin_option == "Samus":
        bomb_sprite = extract_frames(Sbomb_load_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
    
    if bombs_list and bomb_sprite:
        # Calculate the frame index based on the frame counter and bomb duration
        frame_index = (frame_counter // FRAME_DURATION) % num_frames_per_direction
        bomb_frame = bomb_sprite[frame_index]
        
        # Create a surface to blit the bomb sprite onto
        bomb_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        bomb_surface.blit(bomb_frame, (0, 0))  # Blit the bomb frame onto the surface

        screen.blit(bomb_surface, bombs_list[0])

def draw_enemy(screen, enemy):
    pygame.draw.rect(screen, (255, 0, 0), (enemy["x"], enemy["y"], ENEMY_SIZE, ENEMY_SIZE))

