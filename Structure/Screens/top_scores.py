import pygame
def render_top_scores(screen,font, Mbackground, Hbackground, HWIDTH, HHEIGHT):

    #Background slightly gray coated
    overlay = pygame.Surface((HWIDTH, HHEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))
    
    screen.blit(overlay, (0, 0))

    #Insert box
    top_scores_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
    screen.blit(Mbackground, top_scores_bg_rect)

    #Display title text
    title_text = "'¡MEJORES PUNTAJES!"
    title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(HWIDTH/2, HHEIGHT/4))
    title_text_rect.y -= title_surface.get_height() 
    screen.blit(title_surface, title_text_rect)

        # Display exit button
    exit_button_text = "EXIT"
    exit_button_surface = font.render(exit_button_text, True, (255, 255, 0))  # select color
    exit_button_rect = exit_button_surface.get_rect(bottomright=(top_scores_bg_rect.right - 13.75, top_scores_bg_rect.bottom - 19))  # Bottom right corner with some padding
    
    screen.blit(exit_button_surface, exit_button_rect)
