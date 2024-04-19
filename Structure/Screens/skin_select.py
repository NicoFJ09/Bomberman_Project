import pygame
def render_skin_select(screen,font, Mbackground, Hbackground, skins, HWIDTH, HHEIGHT, selected_index):

    #Background slightly gray coated
    screen.blit(Hbackground, (0, 0))
    
    #Insert box
    skin_select_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
    screen.blit(Mbackground, skin_select_bg_rect)

    #Skins
    #if skins[selected_index]

    #Display title text
    title_text = "'¡ESCOGE TU PERSONAJE!"
    title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(HWIDTH/2, HHEIGHT/4))
    title_text_rect.y -= title_surface.get_height() 
    screen.blit(title_surface, title_text_rect)

    

