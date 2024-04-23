import pygame

def render_level_name2(screen, font, WIDTH, HEIGHT):
    global player_position, holding_key, bombs
    # Fill the screen with a solid color (e.g., black)
    screen.fill((0, 0, 0))
    
    # Render a text message at the center of the screen
    text = font.render("level_2", True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center of the screen
    player_position = [240,60]
    holding_key= False
    bombs= 10
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Wait for a few seconds (e.g., 3 seconds)
    pygame.time.wait(3000)  # 3000 milliseconds = 3 seconds
