#Consejos sobre como funciona el juego, objetivo, cajas, cambio de skin, controles, mechanincs, mobs, levels, key, door, etc
import pygame
def render_manual(screen, font, Mbackground, Hbackground, Manual_1, Manual_2, Manual_3, Manual_4, pages, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT, selected_index, y_axis):

    #Background slightly gray coated
    overlay = pygame.Surface((HWIDTH, HHEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))
    
    screen.blit(overlay, (0, 0))

    #Insert box
    manual_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
    screen.blit(Mbackground, manual_bg_rect)

    page_x = (HWIDTH - PAGE_WIDTH) // 2
    page_y = (HHEIGHT - PAGE_HEIGHT) // 2

    #Pages
    if pages[selected_index] == 1:
        screen.blit(Manual_1, (page_x, page_y))
    elif pages[selected_index] == 2:
        screen.blit(Manual_2, (page_x, page_y))
    elif pages[selected_index] == 3:
        screen.blit(Manual_3, (page_x, page_y))
    elif pages[selected_index] == 4:
        screen.blit(Manual_4, (page_x, page_y))
    
    # Display page number text
    page_number_text = f"{selected_index + 1}/{len(pages)}"
    page_number_surface = font.render(page_number_text, True, (26, 140, 24))  # Default color
    page_number_rect = page_number_surface.get_rect(bottomleft=(manual_bg_rect.left + 21.75, manual_bg_rect.bottom - 19))  # Bottom left corner with some padding
    screen.blit(page_number_surface, page_number_rect)

    # Display title text
    title_text = "MANUAL DE JUEGO"
    if y_axis == "IMAGES":
        title_surface = font.render(title_text, True, (255, 255, 0))  # select color
    else: 
        title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(HWIDTH/2, HHEIGHT/4))
    title_text_rect.y -= title_surface.get_height() 
    screen.blit(title_surface, title_text_rect)
    # Display exit button
    exit_button_text = "EXIT"
    if y_axis == "EXIT":
        exit_button_surface = font.render(exit_button_text, True, (255, 255, 0))  # select color
    else:
        exit_button_surface = font.render(exit_button_text, True, (26, 140, 24))  # Default color
    exit_button_rect = exit_button_surface.get_rect(bottomright=(manual_bg_rect.right - 13.75, manual_bg_rect.bottom - 19))  # Bottom right corner with some padding
    
    screen.blit(exit_button_surface, exit_button_rect)

