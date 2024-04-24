from var_consts import *
def draw_door(screen, holding_key, player_position, door_position1, door_position2, door_position3, current_screen, Door):
    global bombs
    # Define door rectangles outside the if statement
    door_rect1 = pygame.Rect(door_position1[0], door_position1[1], BLOCK_SIZE, BLOCK_SIZE)
    door_rect2 = pygame.Rect(door_position2[0], door_position2[1], BLOCK_SIZE, BLOCK_SIZE)
    door_rect3 = pygame.Rect(door_position3[0], door_position3[1], BLOCK_SIZE, BLOCK_SIZE)

    player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
    
    if current_screen == "level_1":
        if player_rect.colliderect(door_rect1) and holding_key:
            # Transition to the next level if holding the key
            holding_key=False
            player_position = [240,60]
            bombs= 10
            return "change_level_2", holding_key, player_position, bombs
    elif current_screen == "level_2":
        if player_rect.colliderect(door_rect2) and holding_key:
            # Transition to the next level if holding the key
            holding_key=False
            player_position = [240,60]
            bombs= 10
            return "change_level_3", holding_key, player_position, bombs
    elif current_screen == "level_3":
        if player_rect.colliderect(door_rect3) and holding_key:
            # You can add code here for additional levels if needed
            holding_key=False
            player_position = [240,60]
            bombs= 15
            return "win", holding_key, player_position, bombs
    
    # Blit the door on the screen
    if current_screen == "level_1":
        screen.blit(Door, door_position1)
    elif current_screen == "level_2":
        screen.blit(Door, door_position2)
    elif current_screen == "level_3":
        screen.blit(Door, door_position3)
    
    # If no transition occurred, return the current screen
    return current_screen, holding_key, player_position, bombs