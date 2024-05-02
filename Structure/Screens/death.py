import pygame

def render_GameOver(screen, font, Mbackground, Hbackground, WIDTH, HEIGHT, skins, skin_lose):
    # Background slightly gray coated
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))

    screen.blit(overlay, (0, 0))

    # Insert box
    settings_bg_rect = Mbackground.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(Mbackground, settings_bg_rect)

    # Render text for "FIN DEL JUEGO" title
    title_text = "FIN DEL JUEGO"
    title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(WIDTH / 2, HEIGHT / 4))
    title_text_rect.y -= title_surface.get_height()
    screen.blit(title_surface, title_text_rect)



    # Render text for "Main Menu" option
    main_menu_text = font.render("Menú Principal", True, (255, 255, 0))
    main_menu_rect = main_menu_text.get_rect(center=(WIDTH // 2, HEIGHT*2 // 3 - 125))
    screen.blit(main_menu_text, main_menu_rect)

    # Depending on the selected_skin_option variable, display the second index of the sprite
    selected_sprite_index = 2  # Index of the sprite to display (second index)
    selected_sprite = skins[skin_lose][selected_sprite_index]

    # Calculate the position to display the sprite
    sprite_rect = selected_sprite.get_rect(midtop=(WIDTH // 2, (main_menu_rect.top + title_text_rect.bottom) // 2))

    sprite_rect.y -= 100  # Adjust this value as needed

    # Blit the selected sprite
    screen.blit(selected_sprite, sprite_rect)
