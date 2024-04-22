# ============================================================= IMPORTS ===================================================================

import pygame
import sys
sys.path.append('../')

#Home imports
from var_consts import *
from Screens.home import render_home
from Screens.settings import render_controls_volume
from Screens.manual import render_manual
from Screens.about import render_about
from Screens.top_scores import render_top_scores
from Screens.user_select import render_user_select

#Main game imports
from Player.controls import handle_player_actions
from Player.display import draw_player, draw_blocks, generate_blocks_positions
from Screens.Levels.Level_1 import render_level_1
from Screens.Levels.Level_constants import *
from Screens.Levels.Level_Name_Display import render_level_name

from Screens.pause import render_pause
# ===================================================================== GAME SETUP ======================================================
pygame.init()


#Window setup
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((HWIDTH,HHEIGHT))

#Home Background
Hbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Home_bg.png").convert_alpha(), (HWIDTH,HHEIGHT))

#Menu Background
Mbackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Menu_bg.png").convert_alpha(), (MWIDTH,MHEIGHT))

#User Background
Ubackground = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/User_bg.png").convert_alpha(), (HWIDTH,HHEIGHT))

#Manual Pages
Manual_1 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_1.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))
Manual_2 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_2.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))
Manual_3 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_3.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))
Manual_4 = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Manual_4.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))

#About Page
About = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/About.png").convert_alpha(), (PAGE_WIDTH,PAGE_HEIGHT))

#Select skin sprites
Bfrontal_1 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Bfrontal_1.png").convert_alpha(), (PAGE_WIDTH*(1/5),PAGE_HEIGHT*(4/9)))
Kfrontal_1 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Kfrontal_1.png").convert_alpha(), (PAGE_WIDTH*(2/9),PAGE_HEIGHT*(1/3)))
Sfrontal_1 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Sfrontal_1.png").convert_alpha(), (PAGE_WIDTH*(2/9),PAGE_HEIGHT*(1/3)))
skin_sprites = {
    "Samus": Sfrontal_1,
    "Bomberman": Bfrontal_1,
    "Kirby": Kfrontal_1
}

#Block sprites
D_block = pygame.transform.scale(pygame.image.load("Assets/Sprites/Destructable_block.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
I_block = pygame.transform.scale(pygame.image.load("Assets/Sprites/Indestructable_block.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))

#Key sprite
Key = pygame.transform.scale(pygame.image.load("Assets/Sprites/Key.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
#Sprite animations
B_down_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_down_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))
B_left_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_left_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))
B_right_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_right_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))
B_up_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_up_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))
B_death_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_death_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))
#Font load
Hfont = pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",30)
TITLE_font = pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",100)
GAME_font =  pygame.font.Font("Assets/Font/PixeloidSans-Bold.ttf",24)
#Music
home_track = "Assets/Sountrack/Home_track.mp3"
level_track = "Assets/Sountrack/Level_track.mp3"
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

    # Base case: no more keys to check
    if not keys:
        return True
    
    # If the new_value is already mapped to another key, return False
    if pygame.key.name(new_value).upper() in options.values():
        return False

    # Recursively check the remaining keys
    return check_keybinds(options, new_value, keys[1:])




def handle_home_controls(selected_index, options, settings_options, selected_option):
   global selection_locked, next_value, blink, y_axis, input_text, music_playing
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
           if selected_option == "MUSIC TOGGLE:":
               if event.key == pygame.key.key_code(settings_options["MOVE LEFT:"]) or event.key == pygame.key.key_code(settings_options["MOVE RIGHT:"]):
                    if options[selected_option] == "<-OFF->":
                        options[selected_option] = "<-ON->"
                        music_playing = True
                    else:
                        options[selected_option] = "<-OFF->"
                        music_playing = False
           else:
               # Append the pressed key to the list
               if check_keybinds(options, next_value):
                   options[selected_option] = (pygame.key.name(next_value).upper())
       else:
           #HOME AND SETTINGS CONTROLS
           if event.key == pygame.key.key_code(settings_options["MOVE UP:"]) and (current_screen == "home" or current_screen == "settings" or current_screen == "paused"):  # Move selection up
               selected_index = (selected_index - 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["MOVE DOWN:"]) and (current_screen == "home" or current_screen == "settings" or current_screen == "paused"):  # Move selection down
               selected_index = (selected_index + 1) % len(options)
            #HOME SPECIFIC CONTROLS
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and (current_screen == "home" or current_screen == "paused"):  # Select option
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
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and (current_screen == "manual" and y_axis=="EXIT") :  # Select option
               selected_option = "EXIT"
               return selected_index, selected_option
           #TOP SCORES AND ABOUT
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and ((current_screen == "about") or (current_screen == "top_scores")):
                selected_option = "EXIT"
                return selected_index, selected_option
           #USER SELECT CONTROLS
           #Skin
           elif event.key == pygame.key.key_code(settings_options["MOVE LEFT:"]) and current_screen == "skin_select":
               selected_index = (selected_index - 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["MOVE RIGHT:"]) and current_screen == "skin_select":
               selected_index = (selected_index + 1) % len(options)
           elif event.key == pygame.key.key_code(settings_options["SELECT:"]) and current_screen == "skin_select":  # Select option
               selected_key = list(skin_sprites.keys())[selected_index]
               selected_option = selected_key
               return selected_index, selected_option
           #User
           elif current_screen == "name_select":
               if event.key == pygame.K_RETURN:
                if len(input_text.strip()) > 0:
                   selected_option = "level_1"
                   selected_index = input_text
                   return selected_index, selected_option
               elif event.key == pygame.K_BACKSPACE:
                   input_text = input_text[:-1]
               else:
                   input_text += event.unicode
               
   return handle_home_controls(selected_index, options, settings_options, selected_option)

#================================================= PLAYER ACTIONS HANDLING ===============================================================================


# ================================================ SCREEN SELECTION HANDLING =============================================================================
def handle_selected_option(selected_option):
   global selection_locked, game_section, selected_skin_option, selected_name, input_text, player_position
   if selected_option == "START":
       return "skin_select" 
   elif selected_option in skin_sprites and current_screen == "skin_select":
       return "name_select"
   elif selected_option == "name_select":
       return "name_select"
   elif selected_option == "level_1":
       game_section= "gameplay"
       return "level_1"
   elif selected_option == "SETTINGS":
       return "settings"
   elif selected_option == "MANUAL":
       return "manual"
   elif selected_option == "TOP SCORES":
       return "top_scores"
   elif selected_option == "ABOUT":
       return "about"
   elif selected_option == "MAIN MENU":
       game_section= "intro"
       return "home"
   elif selected_option in ["MOVE UP:", "MOVE DOWN:", "MOVE LEFT:", "MOVE RIGHT:",
                           "DROP BOMB:", "PAUSE:", "MUSIC TOGGLE:", "SELECT:"] and current_screen=="settings":
       return "settings"
   elif selected_option =="PAUSED":
       game_section= "gameplay"
       return "paused"
   elif selected_option =="RESUME":
       game_section= "gameplay"
       return "level_1"
   elif selected_option == "EXIT (APPLY CHANGES)":
       selection_locked=False
       if game_section== "gameplay":
        return "paused"
       else:
        return "home"
   elif selected_option == "EXIT":
       if game_section== "gameplay":
        return "paused"
       else:
        return "home"
   elif selected_option == "RESTART (A LIFE WILL BE LOST)":
       player_position = [240,60]
       return "level_1"
   elif selected_option == "MAIN MENU (DATA WILL BE LOST IF PRESSED)":
       player_position = [240,60]
       selected_skin_option = ""
       selected_name = ""
       input_text = ""
       return "home"



# ========================================================================== MAIN CODE LOOP ==================================================================

def main():
   global selected_index, Settings_options,Levels, Home_options, selected_option, current_screen, blink, blink_interval, last_blink_time, Initial_entry, y_axis, selected_skin_option, selected_name, music_playing, player_position, game_section, prev_game_section, current_direction, is_moving, frame_counter
   while RUNNING:
       #Handle exit after pressing x
       handle_quit()
       if game_section != prev_game_section:
        prev_game_section = game_section
        music_playing = False  # Reset music_playing to False whenever game_section changes

       if Settings_options["MUSIC TOGGLE:"] == "<-ON->":
        if not music_playing and game_section== "intro":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(home_track)
            pygame.mixer.music.play(-1)  # -1 loops indefinitely
            
        elif not music_playing and  game_section== "gameplay" :  # Check if it's a level screen
            pygame.mixer.music.stop()
            pygame.mixer.music.load(level_track)
            pygame.mixer.music.play(-1)  # -1 loops indefinitely
            
        music_playing = True

       elif Settings_options["MUSIC TOGGLE:"] == "<-OFF->":
        if music_playing:
           pygame.mixer.music.stop()
           music_playing = False
       if Settings_options["MUSIC TOGGLE:"] == "<-ON->": 
           pygame.mixer.music.set_volume(0.5)
       elif Settings_options["MUSIC TOGGLE:"] == "<-OFF->":
           pygame.mixer.music.set_volume(0)
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
           if game_section=="intro":   
            render_controls_volume(screen, Mbackground, Hbackground, Hfont, HWIDTH, HHEIGHT, MHEIGHT, selected_index, Settings_options, blink)
           elif game_section=="gameplay":
               render_controls_volume(screen, Mbackground, Ubackground, Hfont, HWIDTH, HHEIGHT, MHEIGHT, selected_index, Settings_options, blink)       
       #4 ========================================================================= MANUAL RENDERING ========================================================
       elif current_screen == "manual":

           if Initial_entry:
               selected_index = 0
               Initial_entry = False
               y_axis= "IMAGES"

           selected_index, selected_option = handle_home_controls(selected_index, pages, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option)
           if game_section=="intro":   
               render_manual(screen, Hfont, Mbackground, Hbackground, Manual_1, Manual_2, Manual_3, Manual_4, pages, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT, selected_index, y_axis)
           elif game_section=="gameplay":
               render_manual(screen, Hfont, Mbackground, Ubackground, Manual_1, Manual_2, Manual_3, Manual_4, pages, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT, selected_index, y_axis)
       #5 ========================================================================= TOP SCORES RENDERING ========================================================
       elif current_screen == "top_scores":
            if Initial_entry:
               selected_index = 0
               Initial_entry = False
            selected_index, selected_option = handle_home_controls(selected_index, ["EXIT"], Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            if game_section=="intro":
                render_top_scores(screen,Hfont, Mbackground, Hbackground, HWIDTH, HHEIGHT)
            elif game_section=="gameplay":
                render_top_scores(screen,Hfont, Mbackground, Ubackground, HWIDTH, HHEIGHT)
       #6 ========================================================================= ABOUT RENDERING ========================================================
       elif current_screen == "about":
            if Initial_entry:
               selected_index = 0
               Initial_entry = False
            selected_index, selected_option = handle_home_controls(selected_index, ["EXIT"], Settings_options, selected_option)
            current_screen = handle_selected_option(selected_option)
            render_about(screen, Hfont, Mbackground, Hbackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
            if game_section=="intro":
                render_about(screen, Hfont, Mbackground, Hbackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
            elif game_section=="gameplay":
                render_about(screen, Hfont, Mbackground, Ubackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
       #7 ========================================================================= SKIN/NAME SELECT RENDERING ========================================================
       elif current_screen == "skin_select":
            selected_index, selected_option = handle_home_controls(selected_index, skin_sprites, Settings_options, selected_option)
            selected_skin_option = selected_option
            current_screen = handle_selected_option(selected_option)
            render_user_select(screen,Hfont, Mbackground, Ubackground, skin_sprites, HWIDTH, HHEIGHT,PAGE_WIDTH, PAGE_HEIGHT, selected_index, current_screen, input_text)
       elif current_screen == "name_select":
            selected_option = "name_select"
            selected_index, selected_option = handle_home_controls(selected_index, skin_sprites, Settings_options, selected_option)
            selected_name = selected_index
            current_screen = handle_selected_option(selected_option)
            render_user_select(screen,Hfont, Mbackground, Ubackground, skin_sprites, HWIDTH, HHEIGHT,PAGE_WIDTH, PAGE_HEIGHT, selected_index, current_screen, input_text)
       #8 ========================================================================= PAUSE SCREEN ========================================================
       elif current_screen == "paused":
           if Initial_entry:
               selected_index = 0
               Initial_entry = False     
           selected_index, selected_option = handle_home_controls(selected_index, Paused_options, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option)
           render_pause(screen, Ubackground, Hfont, TITLE_font, HWIDTH,HHEIGHT,selected_index, Paused_options)

       #9 ========================================================================= LEVELS RENDERING =================================================================
       elif current_screen == "level_1":
           frame_counter+=1
           screen.fill((26, 140, 24))
           blocks_positions = generate_blocks_positions()
           level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, time, holding_key, bombs)
           player_position, selected_option, is_moving , current_direction  = handle_player_actions(Settings_options, player_position, is_moving, current_direction, blocks_positions)
           current_screen = handle_selected_option(selected_option)
           draw_player(screen, player_position, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, current_direction, is_moving, frame_counter)
           draw_blocks(screen, I_block)
       #Update
       pygame.display.update()
       clock.tick(60)


if __name__ == "__main__":
   main()