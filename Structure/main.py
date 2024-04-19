# ============================================================= IMPORTS ===================================================================

import pygame
import time
import sys
sys.path.append('../')

from var_consts import *
from Screens.home import render_home
from Screens.Levels.Level_1 import render_level_1
from Screens.settings import render_controls_volume
from Screens.manual import render_manual
from Screens.about import render_about
from Screens.top_scores import render_top_scores
from Screens.skin_select import render_skin_select
# ===================================================================== GAME SETUP ======================================================
pygame.init()


#Window setup
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((HWIDTH,HHEIGHT))

#Home Background
Hbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Home_bg.png").convert_alpha(), (HWIDTH,HHEIGHT))

#Menu Background
Mbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Menu_bg.png").convert_alpha(), (MWIDTH,MHEIGHT))

#Manual Pages
Manual_1 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_1.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))
Manual_2 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_2.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))
Manual_3 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_3.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))
Manual_4 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_4.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))

#About Page
About = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/About.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))

#Select skin sprites
Bfrontal_1 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Bfrontal_1.png").convert_alpha(), (PAGE_WIDTH*(1/5),PAGE_HEIGHT*(4/9)))
Kfrontal_1 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Kfrontal_1.png").convert_alpha(), (PAGE_WIDTH*(6/25),PAGE_HEIGHT*(1/3)))
Sfrontal_1 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Sfrontal_1.png").convert_alpha(), (PAGE_WIDTH*(7/25),PAGE_HEIGHT*(21/25)))
#Font load
Hfont = pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",30)

#game ticks setup
clock = pygame.time.Clock()
blink= pygame.time.get_ticks()

# ====================================================== GAME EXIT HANDLING =================================================================
def handle_quit():
   # Check if there are events in the event queue
   if pygame.event.peek(pygame.QUIT):
       event = pygame.event.poll()
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
   # Call handle_events recursively
       return handle_quit()

# ====================================================== TITLE/SETTINGS CONTROL HANDLING ====================================================

def check_keybinds(options, new_value, keys=None):
   if keys is None:
       keys = list(options.keys())

   if not keys:  # Base case: no more keys to check
       return True

   current_key = keys.pop(0)
   if options[current_key] == pygame.key.name(next_value).upper():
       return False
   return check_keybinds(options, new_value, keys)


def handle_home_controls(selected_index, options, settings_options, selected_option):
   global selection_locked, next_value, blink, y_axis
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
           #SETTINGS SPECIFIC CONTROLS
           if selected_option == "SOUND TOGGLE:" or selected_option == "MUSIC TOGGLE:":
               if event.key == pygame.key.key_code(settings_options["MOVE LEFT:"]) or event.key == pygame.key.key_code(settings_options["MOVE RIGHT:"]):
                   options[selected_option] = "<-ON->" if options[selected_option] == "<-OFF->" else "<-OFF->"
           else:
               # Append the pressed key to the list
               if check_keybinds(options, next_value):
                   options[selected_option] = (pygame.key.name(next_value).upper())
       else:
           #HOME AND SETTINGS CONTROLS
           if event.key == pygame.key.key_code(settings_options["MOVE UP:"]) and (current_screen == "home" or current_screen == "settings"):  # Move selection up
               selected_index = (selected_index - 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["MOVE DOWN:"]) and (current_screen == "home" or current_screen == "settings"):  # Move selection down
               selected_index = (selected_index + 1) % len(options)
            #HOME SPECIFIC CONTROLS
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and current_screen == "home":  # Select option
               selected_option = options[selected_index]
               return selected_index, selected_option
           #SETTINGS SPECIFIC CONTROLS
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and current_screen == "settings":  # Select option
               selected_key = list(settings_options.keys())[selected_index]
               selected_option = selected_key
               selection_locked = True
               return selected_index, selected_option
           #MANUAL SPECIFIC CONTROLS
           elif event.key == pygame.key.key_code(settings_options["MOVE LEFT:"]) and current_screen == "manual" and y_axis== "IMAGES":
               selected_index = (selected_index - 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["MOVE RIGHT:"]) and current_screen == "manual" and y_axis== "IMAGES":
               selected_index = (selected_index + 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["MOVE UP:"]) or event.key == pygame.key.key_code(settings_options["MOVE DOWN:"]) and current_screen == "manual":
               y_axis = "IMAGES" if y_axis == "EXIT" else "EXIT"
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and (current_screen == "manual" and y_axis=="EXIT") or (current_screen == "about" and y_axis=="EXIT") or (current_screen == "top_scores" and y_axis=="EXIT")  :  # Select option
               selected_option = "EXIT"
               return selected_index, selected_option
           #SKIN SELECT CONTROLS
           elif event.key == pygame.key.key_code(settings_options["MOVE LEFT:"]) and current_screen == "skin_select":
               selected_index = (selected_index - 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["MOVE RIGHT:"]) and current_screen == "skin_select":
               selected_index = (selected_index + 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and current_screen == "skin_select":  # Select option
               selected_option = options[selected_index]
               return selected_index, selected_option

   return handle_home_controls(selected_index, options, settings_options, selected_option)

# ================================================ SCREEN SELECTION HANDLING =============================================================================
def handle_selected_option(selected_option):
   global selection_locked
   if selected_option == "START":
       return "skin_select" 
   elif selected_option == "SETTINGS":
       return "settings"
   elif selected_option == "MANUAL":
       return "manual"
   elif selected_option == "TOP SCORES":
       return "top_scores"
   elif selected_option == "ABOUT":
       return "about"
   elif selected_option == "MAIN MENU":
       return "home"
   elif selected_option in ["MOVE UP:", "MOVE DOWN:", "MOVE LEFT:", "MOVE RIGHT:",
                           "DROP BOMB:", "PAUSE:", "SOUND TOGGLE:", "MUSIC TOGGLE:", "SELECT:"] and current_screen=="settings":
       return "settings"
   elif selected_option == "EXIT (APPLY CHANGES)":
       selection_locked=False
       return "home"
   elif selected_option == "EXIT":
       return "home"


# ========================================================================== MAIN CODE LOOP ==================================================================

def main():
   global selected_index, Settings_options, special_keys, Home_options, selected_option, current_screen, blink, blink_interval, last_blink_time, Initial_entry, y_axis
   while RUNNING:
       #Handle exit after pressing x
       handle_quit()
        #1 ========================================================================= HOME SCREEN RENDERING =====================================================
       if current_screen == "home":
           Initial_entry = True
           selected_index, selected_option = handle_home_controls(selected_index, Home_options, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option)
           render_home(screen, Hbackground, Hfont, HWIDTH,HHEIGHT,selected_index, Home_options)
        #2 ========================================================================= SETTINGS RENDERING ========================================================
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
           render_controls_volume(screen, Mbackground, Hbackground, Hfont, HWIDTH, HHEIGHT, MHEIGHT, selected_index, Settings_options, blink, special_keys)
        #4 ========================================================================= MANUAL RENDERING ========================================================
       elif current_screen == "manual":

           if Initial_entry:
               selected_index = 0
               Initial_entry = False
               y_axis= "IMAGES"


           selected_index, selected_option = handle_home_controls(selected_index, pages, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option)
           render_manual(screen, Hfont, Mbackground, Hbackground, Manual_1, Manual_2, Manual_3, Manual_4, pages, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT, selected_index, y_axis)
       #5 ========================================================================= TOP SCORES RENDERING ========================================================
       elif current_screen == "top_scores":
            if Initial_entry:
               selected_index = 0
               Initial_entry = False
               y_axis= "EXIT"
            selected_index, selected_option = handle_home_controls(selected_index, pages, Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            render_top_scores(screen,Hfont, Mbackground, Hbackground, HWIDTH, HHEIGHT)
       #6 ========================================================================= ABOUT RENDERING ========================================================
       elif current_screen == "about":
            if Initial_entry:
               selected_index = 0
               Initial_entry = False
               y_axis= "EXIT"
            selected_index, selected_option = handle_home_controls(selected_index, pages, Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            render_about(screen, Hfont, Mbackground, Hbackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
       #7 ========================================================================= SKIN/NAME SELECT RENDERING ========================================================
       elif current_screen == "skin_select":
            selected_index, selected_option = handle_home_controls(selected_index, skins, Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            render_skin_select(screen,Hfont, Mbackground, Hbackground, skins, HWIDTH, HHEIGHT, selected_index)
       #7 ========================================================================= LEVELS RENDERING ========================================================
       elif current_screen == "level_1":
           render_level_1(screen,Hfont, HWIDTH, HHEIGHT)
       #Update
       pygame.display.update()
       clock.tick(60)


if __name__ == "__main__":
   main()