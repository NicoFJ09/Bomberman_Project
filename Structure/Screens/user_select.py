import pygame

def render_user_select(screen,font, Mbackground, Ubackground, skins , HWIDTH, HHEIGHT,PAGE_WIDTH, PAGE_HEIGHT, selected_index, current_screen, input_text):

    # Background slightly gray coated
    screen.blit(Ubackground, (0, 0))
    
    # Insert box
    skin_select_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
    screen.blit(Mbackground, skin_select_bg_rect)

    # Display title text for skin selection
    skin_title_text = "¡ESCOGE TU PERSONAJE!"
    skin_title_surface = font.render(skin_title_text, True, (26, 140, 24))  # Default color
    skin_title_text_rect = skin_title_surface.get_rect(midtop=(HWIDTH // 2, HHEIGHT // 4))
    skin_title_text_rect.y -= skin_title_surface.get_height() 
    screen.blit(skin_title_surface, skin_title_text_rect)

    # Display title text for name selection
    name_title_text = "¡SELECCIONA TU NOMBRE!"
    name_title_surface = font.render(name_title_text, True, (26, 140, 24))  # Default color
    name_title_text_rect = name_title_surface.get_rect(midtop=(HWIDTH // 2, HHEIGHT // 1.5))
    name_title_text_rect.y -= name_title_surface.get_height() 
    screen.blit(name_title_surface, name_title_text_rect)

        # Define dimensions for the text box
    text_box_width = 350
    text_box_height = 40
    text_box_rect = pygame.Rect((HWIDTH - text_box_width) // 2, name_title_text_rect.bottom + 30, text_box_width, text_box_height)
    pygame.draw.rect(screen, (26, 140, 24), text_box_rect, 3)

    #Reference point
    invisible_rectangle = pygame.Surface((PAGE_WIDTH, PAGE_HEIGHT), pygame.SRCALPHA)
    invisible_rectangle_rect = invisible_rectangle.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))

    skin_coordinates = {
        "Bomberman": (282.5, 25),
        "Kirby": (465, 175),
        "Samus": (86.5, 175)
    }
    invisible_rectangle.blit(skins["Samus"], (skin_coordinates["Samus"]))
    invisible_rectangle.blit(skins["Bomberman"], (skin_coordinates["Bomberman"]))
    invisible_rectangle.blit(skins["Kirby"], (skin_coordinates["Kirby"]))
    if current_screen == "skin_select":
        if list(skins.keys())[selected_index] == "Bomberman":
            pygame.draw.rect(invisible_rectangle, (255, 255, 0), (282.5-10, 25-10, skins["Bomberman"].get_width()+20, skins["Bomberman"].get_height()+20), 3)
        elif list(skins.keys())[selected_index] == "Kirby":
            pygame.draw.rect(invisible_rectangle, (255, 255, 0), (465-10, 175-10, skins["Kirby"].get_width()+20, skins["Kirby"].get_height()+20), 3)
        elif list(skins.keys())[selected_index] == "Samus":
            pygame.draw.rect(invisible_rectangle, (255, 255, 0), (86.5-10, 175-10, skins["Samus"].get_width()+20, skins["Samus"].get_height()+20), 3)
    elif current_screen == "name_select":
        pygame.draw.rect(screen, (255, 255, 0), text_box_rect, 3)
        # Render and display entered text
        entered_text = input_text[:14]  # Limit the input text to 20 characters
        entered_text_surface = font.render(entered_text, True, (91, 101, 113))
        entered_text_rect = entered_text_surface.get_rect(center=text_box_rect.center)  # Centering the text
        screen.blit(entered_text_surface, entered_text_rect)
        input_text = entered_text
    # Blit the invisible rectangle onto the screen
    screen.blit(invisible_rectangle, invisible_rectangle_rect)

    pygame.display.flip()
