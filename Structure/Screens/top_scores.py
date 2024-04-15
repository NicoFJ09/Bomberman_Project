import pygame
def render_top_scores(screen, Mbackground, Hbackground, WIDTH, HEIGHT):

    #Background slightly gray coated
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))
    
    screen.blit(overlay, (0, 0))

    #Insert box
    settings_bg_rect = Mbackground.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(Mbackground, settings_bg_rect)