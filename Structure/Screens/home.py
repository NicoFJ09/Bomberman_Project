def render_home(screen, background, font, WIDTH, HEIGHT):
    screen.blit(background, (0, 0))
    text_surface = font.render("START", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)