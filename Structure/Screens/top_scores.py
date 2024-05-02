import pygame
import os

def render_top_scores(screen, font, Mbackground, Hbackground, HWIDTH, HHEIGHT):
    # Background slightly gray coated
    overlay = pygame.Surface((HWIDTH, HHEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 128))
    screen.blit(Hbackground, (0, 0))
    screen.blit(overlay, (0, 0))

    # Insert box
    top_scores_bg_rect = Mbackground.get_rect(center=(HWIDTH // 2, HHEIGHT // 2))
    screen.blit(Mbackground, top_scores_bg_rect)

    # Display title text
    title_text = "TOP SCORES"
    title_surface = font.render(title_text, True, (26, 140, 24))  # Default color
    title_text_rect = title_surface.get_rect(midtop=(HWIDTH/2, HHEIGHT/4))
    screen.blit(title_surface, title_text_rect)

    # Display exit button
    exit_button_text = "EXIT"
    exit_button_surface = font.render(exit_button_text, True, (255, 255, 0))  # select color
    exit_button_rect = exit_button_surface.get_rect(bottomright=(top_scores_bg_rect.right - 13.75, top_scores_bg_rect.bottom - 19))  # Bottom right corner with some padding
    screen.blit(exit_button_surface, exit_button_rect)

    # Display top scores
    file_path = get_file_path()
    scores = read_scores(file_path)
    y_offset = title_text_rect.bottom -  60  # Initial y offset without extra padding
    spacing = (top_scores_bg_rect.bottom - (y_offset+25)) / 6  # Equal spacing for 6 sections (title + 5 scores)

    render_scores(screen, font, scores, HWIDTH, y_offset, spacing)

def render_scores(screen, font, scores, HWIDTH, y_offset, spacing, count=0):
    if count >= 5:
        return

    if scores:
        name, score = scores[0]
        score_text = f"{name} : {score}"
        score_surface = font.render(score_text, True, (235, 129, 63))  # Score color
        score_rect = score_surface.get_rect(midtop=(HWIDTH/2, y_offset + (count + 1) * spacing))
        screen.blit(score_surface, score_rect)
        render_scores(screen, font, scores[1:], HWIDTH, y_offset, spacing, count + 1)
    else:
        empty_text = "EMPTY"
        empty_surface = font.render(empty_text, True, (235, 129, 63))  # Score color
        empty_rect = empty_surface.get_rect(midtop=(HWIDTH/2, y_offset + (count + 1) * spacing))
        screen.blit(empty_surface, empty_rect)
        render_scores(screen, font, [], HWIDTH, y_offset, spacing, count + 1)

def read_scores(file_path):
    scores = []

    def read_score_line(file_obj, count=0):
        if count >= 5:  # Limit to the first 5 scores
            return

        line = file_obj.readline()
        if line:
            parts = line.strip().split(' : ')
            if len(parts) == 2:
                scores.append((parts[0], int(parts[1])))
                read_score_line(file_obj, count + 1)

    try:
        with open(file_path, 'r') as archivo:
            read_score_line(archivo)
    except FileNotFoundError:
        pass  # No file found, scores list will be empty

    return scores

def get_file_path():
    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(parent_directory)

    # Create the file path relative to the parent directory
    file_path = os.path.join(parent_directory, 'scores.txt')
    return file_path

# Test the function
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)
Mbackground = pygame.Surface((400, 300))
Hbackground = pygame.Surface((800, 600))
HWIDTH, HHEIGHT = 800, 600
render_top_scores(screen, font, Mbackground, Hbackground, HWIDTH, HHEIGHT)
pygame.display.flip()
