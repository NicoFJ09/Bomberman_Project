#Pantalla inicio
def render_home_aux(screen, font, screen_height, options, x, y, index, hovered_index):
   if index >= len(options):
       return
  
   # Calcular espacio total  sobrante entre texto
   total_height = screen_height*2/3 - (font.size(options[0])[1] * len(options))


   # Calcular distancia entre opciones
   gap = (total_height / (len(options))) + font.size(options[0])[1]


   # Calcular coordenada y entre opciones
   y += gap


   # Opcion actual para renderizar y blit
   if index == hovered_index:
       text_surface = font.render(options[index], True, (255, 255, 0))  # Yellow color for selected option
   else:
       text_surface = font.render(options[index], True, (26, 140, 24))  # Default color for unselected options
  
   text_rect = text_surface.get_rect(midtop=(x ,y))
  
   screen.blit(text_surface, text_rect)


   # Renderizar siguiende opcion recursivamente
   return render_home_aux(screen, font, screen_height, options, x, y, index + 1, hovered_index)


def render_home(screen, Hbackground, font, WIDTH, HEIGHT, hovered_index, options):
   screen.blit(Hbackground, (0, 0))


   # Calcular coordenada y para insertar texto
   y = (HEIGHT/ 4) - font.size(options[0])[1]


   # Calcular coordenada x para todas opciones
   x= WIDTH/2

   version_text = "EL HOMBRE BOMBA V3.0.0"
   version_surface = font.render(version_text, True, (235, 129, 63)) 
   version_rect = version_surface.get_rect(topleft=(10, HEIGHT - 50))  # Bottom left corner with some padding
   screen.blit(version_surface, version_rect)

   info_text = "© 2024 | COSTA RICA"
   info_surface = font.render(info_text, True, (235, 129, 63)) 
   info_rect = info_surface.get_rect(topright=(WIDTH-10, HEIGHT - 50))  # Bottom left corner with some padding
   screen.blit(info_surface, info_rect)
   #Renderizar opciones
   return render_home_aux(screen, font, HEIGHT, options, x, y, 0, hovered_index)




