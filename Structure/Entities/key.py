import pygame
from var_consts import *

def draw_key(screen, holding_key, player_position, key_position1, key_position2, key_position3, current_screen, Key):
    # Define key rectangles outside the if statement
    key_rect1 = pygame.Rect(key_position1[0]+BLOCK_SIZE//6, key_position1[1]+BLOCK_SIZE//6, (BLOCK_SIZE)//3, (BLOCK_SIZE)//3)
    key_rect2 = pygame.Rect(key_position2[0]+BLOCK_SIZE//6, key_position2[1]+BLOCK_SIZE//6, (BLOCK_SIZE)//3, (BLOCK_SIZE)//3)
    key_rect3 = pygame.Rect(key_position3[0]+BLOCK_SIZE//6, key_position3[1]+BLOCK_SIZE//6, (BLOCK_SIZE)//3, (BLOCK_SIZE)//3)

    player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
    
    if current_screen == "level_1":
        if player_rect.colliderect(key_rect1):
            holding_key = True
    elif current_screen == "level_2":
        if player_rect.colliderect(key_rect2):
            holding_key = True
    elif current_screen == "level_3":
        if player_rect.colliderect(key_rect3):
            holding_key = True
    
    # Blit the key on the screen only if holding_key is False
    if not holding_key:
        if current_screen == "level_1":
            screen.blit(Key, key_position1)
        elif current_screen == "level_2":
            screen.blit(Key, key_position2)
        elif current_screen == "level_3":
            screen.blit(Key, key_position3)
    
    return holding_key