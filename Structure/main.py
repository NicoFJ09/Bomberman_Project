import pygame
import sys
sys.path.append('../')

from var_consts import *

from Screens.home import render_home

from Screens.Levels.Level_1 import render_level_1

from Screens.settings import render_controls_volume

pygame.init()

#Window setup 
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((HWIDTH,HHEIGHT))

#Home Background
Hbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Home_bg.png").convert_alpha(), (HWIDTH,HHEIGHT))

#Menu Background
Mbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Menu_bg.png").convert_alpha(), (MWIDTH,MHEIGHT))
#Font load
font = pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",30)

#game ticks setup
clock = pygame.time.Clock()
blink= pygame.time.get_ticks()

#DETECTAR SALIR JUEGO

def handle_quit():
    # Check if there are events in the event queue
    if pygame.event.peek(pygame.QUIT):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Call handle_events recursively
        return handle_quit()

def check_keybinds(options, new_value):
    for key in options:
        if options[key] == chr(new_value).upper():
            return False
    return True
#Compara para revisar si hay repetidos
    
#DETECTAR MOVIMIENTOS EN HOME
def handle_home_controls(selected_index, options, settings_options, selected_option):
    global selection_locked, next_value, blink
    events = pygame.event.get()

    if not events:  # Base case: No more events
        return selected_index, selected_option  # Return toggle_index as well
    event = events.pop(0)  # Get the first event

    if event.type == pygame.KEYDOWN:
        if selection_locked:
            next_value = event.key
            blink = True
            selection_locked = False
            selected_option = list(options.keys())[selected_index]
            if selected_option == "SOUND TOGGLE:" or selected_option == "MUSIC TOGGLE:":
                if event.key == pygame.key.key_code(settings_options["MOVE LEFT:"]) or event.key == pygame.key.key_code(settings_options["MOVE RIGHT:"]):
                    options[selected_option] = "<-ON->" if options[selected_option] == "<-OFF->" else "<-OFF->"
            else:
                # Append the pressed key to the list
                if check_keybinds(options, next_value):
                    options[selected_option] = (pygame.key.name(next_value).upper())
                else: 
                    print("value is already assigned to another key!")
        else: 
            if event.key == pygame.key.key_code(settings_options["MOVE UP:"]):  # Move selection up
                selected_index = (selected_index - 1) % len(options)
            elif event.key == pygame.key.key_code(settings_options["MOVE DOWN:"]):  # Move selection down
                selected_index = (selected_index + 1) % len(options)
            elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and current_screen == "home":  # Select option
                selected_option = options[selected_index]
                return selected_index, selected_option
            elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and current_screen == "settings":  # Select option
                selected_key = list(settings_options.keys())[selected_index]
                selected_option = selected_key
                selection_locked = True
                return selected_index, selected_option

    return handle_home_controls(selected_index, options, settings_options, selected_option)

def handle_selected_option(selected_option):
    global selection_locked
    if selected_option == "START":
        return "level_1"  # Update current screen to level 1
    elif selected_option == "SETTINGS":
        return "settings"
    elif selected_option == "MANUAL":
        return "manual"
    elif selected_option == "TOP_SCORES":
        return "top_scores"
    elif selected_option == "ABOUT":
        return "about"
    elif selected_option == "MAIN MENU":
        return "home"
    elif selected_option in ["MOVE UP:", "MOVE DOWN:", "MOVE LEFT:", "MOVE RIGHT:",
                            "DROP BOMB:", "DETONATE BOMB:", "PAUSE:", "SOUND TOGGLE:", "MUSIC TOGGLE:", "SELECT:"]:
        return "settings"
    elif selected_option == "EXIT (APPLY CHANGES)":
        selection_locked=False
        return "home"

def main():
    global selected_index, Settings_options, special_keys, Home_options, selected_option, current_screen, blink, blink_interval, last_blink_time, Initial_entry
    while RUNNING:
        # Handle exit after pressing x
        handle_quit()
        #1 Home screen rendering
        if current_screen == "home":
            Initial_entry = True
            selected_index, selected_option = handle_home_controls(selected_index, Home_options, Settings_options, selected_option)
            current_screen= handle_selected_option(selected_option)
            render_home(screen, Hbackground, font, HWIDTH,HHEIGHT,selected_index, Home_options)
        #2 Settings rendering
        elif current_screen == "settings":
                # Toggle blinking state based on timer
            current_time = pygame.time.get_ticks()
            if selection_locked and current_time - last_blink_time > blink_interval:
                blink = not blink
                last_blink_time = current_time
                    
            if Initial_entry:
                selected_index = 0
                Initial_entry = False            

            selected_index, selected_option = handle_home_controls(selected_index, Settings_options, Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            render_controls_volume(screen, Mbackground, Hbackground, font, HWIDTH, HHEIGHT, MHEIGHT, selected_index, Settings_options, blink, special_keys)

        elif current_screen == "manual":
            pass
        elif current_screen == "top_scores":
            pass
        elif current_screen == "about":
            pass
        elif current_screen == "level_1":
            render_level_1(screen,font, HWIDTH, HHEIGHT)
        #Update
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()