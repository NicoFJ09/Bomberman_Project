import pygame
from var_consts import *

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


def draw_player(screen, player_position, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, current_direction, is_moving, frame_counter):
    if selected_skin_option == "Bomberman":
        if current_direction == "UP":
            frames = extract_frames(B_up_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "DOWN":
            frames = extract_frames(B_down_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "LEFT":
            frames = extract_frames(B_left_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        elif current_direction == "RIGHT":
            frames = extract_frames(B_right_sprite, num_frames_per_direction, BLOCK_SIZE, BLOCK_SIZE)
        
        if is_moving:
            screen.blit(frames[(frame_counter // FRAME_DURATION) % num_frames_per_direction], player_position)
        else:
            screen.blit(frames[0], player_position)  # Draw idle frame

def generate_blocks_positions():
    blocks_positions = []
    
    # Generate blocks for all even rows and columns
    for y in range(0, HHEIGHT, BLOCK_SIZE * 2):
        row = []
        for x in range(180, HWIDTH, BLOCK_SIZE * 2):
            row.append((x, y))  # Add block position
        blocks_positions.append(row)
    
    # Append blocks to the first and last rows
    for x in range(180, HWIDTH, BLOCK_SIZE):
        blocks_positions[0].append((x, 0))
        blocks_positions[-1].append((x, HHEIGHT - BLOCK_SIZE))
    
    # Append blocks to the first and last columns
    for y in range(0, HHEIGHT, BLOCK_SIZE):
        for row in blocks_positions:
            row.append((180, y))
            row.append((HWIDTH - BLOCK_SIZE, y))
    
    return blocks_positions


def draw_blocks(screen, BLOCK_SPRITE):
    blocks_positions = generate_blocks_positions()
    for row in blocks_positions:
        for x, y in row:
            screen.blit(BLOCK_SPRITE, (x, y))