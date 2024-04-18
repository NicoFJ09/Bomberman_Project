#Informacion del TEC, carrera, curso, año, profesor, pais de produccion and version
import pygame
def render_about(screen, font, Mbackground, Hbackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT):

    #Background slightly gray coated
    overlay = pygame.Surface((HWIDTH, HHEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))
    
    screen.blit(overlay, (0, 0))

    #Insert box
    About_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
    screen.blit(Mbackground, About_bg_rect)

    
    page_x = (HWIDTH - PAGE_WIDTH) // 2
    page_y = (HHEIGHT - PAGE_HEIGHT) // 2

    screen.blit(About,(page_x,page_y))

    # Display title text
    title_text = "CONOCE AL CREADOR"
    title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(HWIDTH/2, HHEIGHT/4))
    title_text_rect.y -= title_surface.get_height() 
    screen.blit(title_surface, title_text_rect)

    # Display exit button
    exit_button_text = "EXIT"
    exit_button_surface = font.render(exit_button_text, True, (255, 255, 0))  # select color
    exit_button_rect = exit_button_surface.get_rect(bottomright=(About_bg_rect.right - 13.75, About_bg_rect.bottom - 19))  # Bottom right corner with some padding
    
    screen.blit(exit_button_surface, exit_button_rect)
