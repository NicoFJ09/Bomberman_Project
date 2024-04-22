import pygame

def level_constants(screen, font, WIDTH, HEIGHT, points, lives, time, holding_key, bombs):
    # Fill the screen with a solid color (e.g., green for the game background)
    screen.fill((26, 140, 24))  # Green background

    # Define the dimensions and position of the info box
    info_box_width = 180
    info_box_color = (170, 191, 208)  # Gray color for the info box
    info_box_rect = pygame.Rect(0, 0, info_box_width, HEIGHT)  # Adjusted for vertical orientation

    # Draw the info box
    pygame.draw.rect(screen, info_box_color, info_box_rect)

    # Render text for the information to display inside the box
    points_text = font.render(f"Points: {points}", True, (255, 255, 0))  # Yellow text color
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 0))  # Yellow text color
    time_text = font.render(f"Time: {time}", True, (255, 255, 0))  # Yellow text color
    key_text = font.render(f"Key: {holding_key}", True, (255, 255, 0))  # Yellow text color
    bombs_text = font.render(f"Bombs: {bombs}", True, (255, 255, 0))  # Yellow text color

    # Define the positions of the text inside the info box
    text_margin = 140
    points_text_rect = points_text.get_rect(topleft=(10, 10))
    lives_text_rect = lives_text.get_rect(topleft=(10, points_text_rect.bottom + text_margin))
    bombs_text_rect = bombs_text.get_rect(topleft=(10, lives_text_rect.bottom + text_margin))
    time_text_rect = time_text.get_rect(topleft=(10, bombs_text_rect.bottom + text_margin))  
    key_text_rect = key_text.get_rect(topleft=(10, time_text_rect.bottom + text_margin))  
    
    # Blit the text onto the screen
    screen.blit(points_text, points_text_rect)
    screen.blit(lives_text, lives_text_rect)
    screen.blit(bombs_text, bombs_text_rect)
    screen.blit(time_text, time_text_rect)
    screen.blit(key_text, key_text_rect)
