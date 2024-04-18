import pygame
def render_controls_volume_aux(screen, font, screen_height, options, x, y, index, hovered_index,blink, special_keys):
   if index>= len(options):
       return
 
   # Calcular espacio total  sobrante entre texto
   total_height = screen_height*5/6 - (font.size(next(iter(options.keys())))[1] * len(options))

   # Calcular distancia entre opciones
   gap = (total_height / (len(options))-2) + font.size(next(iter(options.keys())))[1]

   key = list(options.keys())[index]
   value = options[key]
   if value in special_keys:
       value = special_keys[value]
   option_text= f"{key} {value}"

   if index == hovered_index:
       if blink:
           text_surface = font.render(option_text, True, (255, 255, 0))  #Yellow selected
       else:
           text_surface = font.render("", True, (255, 255, 0))
   else:
       text_surface = font.render(option_text, True, (26, 140, 24))  # Default color
 
   text_rect = text_surface.get_rect(midtop=(x ,y))
 
   screen.blit(text_surface, text_rect)
   y+=gap

   return render_controls_volume_aux(screen, font, screen_height, options, x, y, index+1, hovered_index,blink, special_keys)



def render_controls_volume(screen, Mbackground, Hbackground, font, HWIDTH, HHEIGHT, MHEIGHT, hovered_index, Settings_options,blink, special_keys):
   #Background slightly gray coated
   overlay = pygame.Surface((HWIDTH, HHEIGHT), pygame.SRCALPHA)
   overlay.fill((128, 128, 128, 128))
   screen.blit(Hbackground, (0, 0))
   screen.blit(overlay, (0, 0))

   #Insert box
   settings_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
   screen.blit(Mbackground, settings_bg_rect)

   #Top text 
   anouncement_text = font.render("PERSONALIZA TECLAS (NO REPETIR VALORES)", True, (26, 140, 24))
   anouncement_text_text_rect = anouncement_text.get_rect(center=(HWIDTH // 2, 130))
   screen.blit(anouncement_text, anouncement_text_text_rect)

   # Calcular coordenada y para insertar texto
   y = HHEIGHT/4 - font.size(next(iter(Settings_options.keys())))[1]
   # Calcular coordenada x para todas opciones
   x=  HWIDTH/2
 
   return render_controls_volume_aux(screen, font, MHEIGHT, Settings_options, x, y, 0, hovered_index, blink, special_keys)
