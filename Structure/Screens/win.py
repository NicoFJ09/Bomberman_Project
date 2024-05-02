import pygame
from var_consts import *
def render_Win(screen, font, Mbackground, Hbackground, WIDTH, HEIGHT,skins,skin_win, W_points,minutes, seconds):
    # Background slightly gray coated
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))

    screen.blit(overlay, (0, 0))

    # Insert box
    settings_bg_rect = Mbackground.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(Mbackground, settings_bg_rect)

    # Render text for "FIN DEL JUEGO" title
    title_text = "¡GANASTE!"
    title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(WIDTH / 2, HEIGHT / 4))
    title_text_rect.y -= title_surface.get_height()
    screen.blit(title_surface, title_text_rect)

    # Render text for "Main Menu" option
    main_menu_text = font.render("Menú Principal", True, (255, 255, 0))
    W_points_text = font.render(f"Final points: {W_points}", True, (26, 140, 24))
    F_time_text = font.render(f"Final time: {minutes}:{seconds}", True, (26, 140, 24))

    # Calculate vertical positions
    available_height = HEIGHT - (2/3 * HEIGHT)  # Available space from 2/3 of the screen to the bottom
    spacing = available_height / 8  # Divide available space equally for each text element

    # Update vertical positions for each text element
    main_menu_rect = main_menu_text.get_rect(midbottom=(WIDTH // 2, (5/6 * HEIGHT)))
    F_time_text_rect = F_time_text.get_rect(midbottom=(WIDTH // 2, main_menu_rect.top - spacing))
    W_points_text_rect = W_points_text.get_rect(midbottom=(WIDTH // 2, F_time_text_rect.top - spacing))

    # Depending on the selected_skin_option variable, display the second index of the sprite
    selected_sprite_index = 1  # Index of the sprite to display (second index)
    selected_sprite = skins[skin_win][selected_sprite_index]

    # Calculate the position to display the sprite
    sprite_rect = selected_sprite.get_rect(midtop=(WIDTH // 2, (W_points_text_rect.top + title_text_rect.bottom) // 2))

    sprite_rect.y -= 125  # Adjust this value as needed

    # Blit the selected sprite
    screen.blit(selected_sprite, sprite_rect)


    # Blit text to the screen
    screen.blit(main_menu_text, main_menu_rect)
    screen.blit(W_points_text, W_points_text_rect)
    screen.blit(F_time_text, F_time_text_rect)