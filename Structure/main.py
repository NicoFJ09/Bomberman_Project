# ============================================================= IMPORTS ===================================================================

import pygame
import sys
sys.path.append('../')

import time
game_time=0

#Home imports
from var_consts import *
from Screens.home import render_home
from Screens.settings import render_controls_volume
from Screens.manual import render_manual
from Screens.about import render_about
from Screens.top_scores import render_top_scores
from Screens.user_select import render_user_select

#Main game imports
from Player.controls import handle_player_actions, handle_bomb_explosion, draw_enemies, create_enemy, update_enemy_position
from Player.display import draw_player, draw_blocks, draw_bombs
from Screens.Levels.Level_constants import *
from Screens.Levels.Level_Name_Display import render_level_name
from Screens.Levels.Level_Name_Display2 import render_level_name2
from Screens.Levels.Level_Name_Display3 import render_level_name3
from Screens.death import render_GameOver
from Screens.win import render_Win

from Entities.key import draw_key
from Entities.door import draw_door
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
#DOORWAY
doorway = pygame.transform.scale(pygame.image.load("Assets/Sprites/doorway.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
#Sprite animations
B_down_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_down_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
B_left_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_left_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
B_right_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_right_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
B_up_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/B_up_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))

K_down_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/K_down_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
K_left_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/K_left_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
K_right_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/K_right_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
K_up_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/K_up_sprite.png").convert_alpha(), (BLOCK_SIZE*3,60))

S_left_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/S_left_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
S_right_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/S_right_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))

#ENEMY ANIMATIONS
Enemy_1_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_1_sprite.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
Enemy_2_down_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_2_down_sprite.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
#bomb
Kbomb_load_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Kbomb_load_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
Bbomb_load_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Bbomb_load_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
Sbomb_load_sprite =  pygame.transform.scale(pygame.image.load("Assets/Sprites/Sbomb_load_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))

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
                   selected_option = "change_level_1"
                   selected_index = input_text
                   return selected_index, selected_option
               elif event.key == pygame.K_BACKSPACE:
                   input_text = input_text[:-1]
               else:
                   input_text += event.unicode

        #END AND WIN SCREENS
           elif current_screen == "game_over" or current_screen == "win":

            if event.key == pygame.key.key_code(settings_options["SELECT:"]):
                selected_option = options[selected_index]
                return selected_index, selected_option

   return handle_home_controls(selected_index, options, settings_options, selected_option)

#================================================= PLAYER ACTIONS HANDLING ===============================================================================


# ================================================ SCREEN SELECTION HANDLING =============================================================================
def handle_selected_option(selected_option, previous_screen):
   global selection_locked, game_section, selected_skin_option, selected_name, input_text, player_position, holding_key, bombs, game_time, lives, enemy_x, enemy_y, enemy2_x, enemy2_y, enemy3_y, enemy3_x, Dblocks_positions1, Dblocks_positions2, Dblocks_positions3
   if selected_option == "START":
       return "skin_select" 
   
   elif selected_option in skin_sprites and current_screen == "skin_select":
       return "name_select"
   
   elif selected_option == "name_select":
       return "name_select"
   
   elif selected_option == "change_level_1":
       render_level_name(screen, Hfont, HWIDTH, HHEIGHT)
       enemy_x, enemy_y = 240, 420  # Adjust the coordinates as needed
       enemy2_x, enemy2_y = 780, 660
       enemy3_x, enemy3_y = 960, 120
       return "level_1"
   elif selected_option == "change_level_2":
       render_level_name2(screen, Hfont, HWIDTH, HHEIGHT)
       enemy_x, enemy_y = 360, 540  # Adjust the coordinates as needed
       enemy2_x, enemy2_y = 540, 180
       enemy3_x, enemy3_y = 780, 300
       return "level_2"
   elif selected_option == "change_level_3":
       render_level_name3(screen, Hfont, HWIDTH, HHEIGHT)
       enemy_x, enemy_y = 540, 180  # Adjust the coordinates as needed
       enemy2_x, enemy2_y = 960, 120
       enemy3_x, enemy3_y = 360, 540
       return "level_3"
   
   elif selected_option == "level_1":
       game_section= "gameplay"
       return "level_1"
   
   elif selected_option == "level_2":
       game_section= "gameplay"
       return "level_2"
   
   elif selected_option == "level_3":
       game_section= "gameplay"
       return "level_3"   

   elif selected_option == "win":
       game_section= "gameplay"
       return "win"   
   
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
       return previous_screen
   
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
   elif selected_option == "RESTART (WILL RETURN TO LEVEL 1)":
       player_position = [240,60]
       game_time = 0
       return "level_1"
   elif selected_option == "DEATH":
       return "game_over"
   elif selected_option == "MAIN MENU (DATA WILL BE LOST IF PRESSED)":
       Dblocks_positions1= [[(240, 480), (600, 480)], [(300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420)], [(360, 360), (600, 360), (960, 360)], [(240, 300), (300, 300), (420, 300), (960, 300)], [(900, 780), (960, 780), (1080, 780)], [(900, 60), (1080, 60)], [(480, 240), (600, 240), (720, 240), (780, 240), (1080, 240)], [(600, 720), (720, 720)], [(300, 180), (360, 180), (600, 180), (900, 180), (1080, 180)], [(360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660)], [(720, 600)], [(720, 540), (960, 540), (1080, 540)]]

       Dblocks_positions2= [[(240, 480), (600, 480)], [(300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420)], [(360, 360), (600, 360), (960, 360)], [(240, 300), (300, 300), (420, 300), (960, 300)], [(900, 780), (960, 780), (1080, 780)], [(900, 60), (1080, 60)], [(480, 240), (600, 240), (720, 240), (780, 240), (1080, 240)], [(600, 720), (720, 720)], [(300, 180), (360, 180), (600, 180), (900, 180), (1080, 180)], [(360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660)], [(720, 600)], [(720, 540), (960, 540), (1080, 540)]]

       Dblocks_positions3= [[(240, 480), (600, 480)], [(300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420)], [(360, 360), (600, 360), (960, 360)], [(240, 300), (300, 300), (420, 300), (960, 300)], [(900, 780), (960, 780), (1080, 780)], [(900, 60), (1080, 60)], [(480, 240), (600, 240), (720, 240), (780, 240), (1080, 240)], [(600, 720), (720, 720)], [(300, 180), (360, 180), (600, 180), (900, 180), (1080, 180)], [(360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660)], [(720, 600)], [(720, 540), (960, 540), (1080, 540)]]

       player_position = [240,60]
       lives = 3
       bombs =15
       selected_skin_option = ""
       selected_name = ""
       input_text = ""
       game_section= "intro"
       return "home"



# ========================================================================== MAIN CODE LOOP ==================================================================

def main():
   global selected_index, Settings_options,Levels, Home_options, selected_option, current_screen, blink, blink_interval, last_blink_time, Initial_entry, y_axis, selected_skin_option, selected_name, music_playing, player_position, game_section, prev_game_section, current_direction, is_moving, frame_counter, holding_key, bombs, previous_screen, Dblocks_positions1, game_time, lives, LEVEL_1_ENEMIES, WINNER, W_points
   while RUNNING:
       #Handle exit after pressing x
       handle_quit()
       global game_time
       game_time += clock.get_rawtime() / 1000
       game_time = round(game_time, 2)
       if game_section != prev_game_section:

        prev_game_section = game_section
        if game_section == "gameplay":
            game_time = 0
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
           current_screen = handle_selected_option(selected_option, previous_screen)
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
           current_screen = handle_selected_option(selected_option, previous_screen)
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
           current_screen = handle_selected_option(selected_option, previous_screen)
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
            current_screen = handle_selected_option(selected_option, previous_screen)
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
            current_screen = handle_selected_option(selected_option, previous_screen)
            render_about(screen, Hfont, Mbackground, Hbackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
            if game_section=="intro":
                render_about(screen, Hfont, Mbackground, Hbackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
            elif game_section=="gameplay":
                render_about(screen, Hfont, Mbackground, Ubackground, About, HWIDTH, HHEIGHT, PAGE_WIDTH, PAGE_HEIGHT)
       #7 ========================================================================= SKIN/NAME SELECT RENDERING ========================================================
       elif current_screen == "skin_select":
            selected_index, selected_option = handle_home_controls(selected_index, skin_sprites, Settings_options, selected_option)
            selected_skin_option = selected_option
            current_screen = handle_selected_option(selected_option, previous_screen)
            render_user_select(screen,Hfont, Mbackground, Ubackground, skin_sprites, HWIDTH, HHEIGHT,PAGE_WIDTH, PAGE_HEIGHT, selected_index, current_screen, input_text)
       elif current_screen == "name_select":
            selected_option = "name_select"
            selected_index, selected_option = handle_home_controls(selected_index, skin_sprites, Settings_options, selected_option)
            selected_name = selected_index
            current_screen = handle_selected_option(selected_option, previous_screen)
            render_user_select(screen,Hfont, Mbackground, Ubackground, skin_sprites, HWIDTH, HHEIGHT,PAGE_WIDTH, PAGE_HEIGHT, selected_index, current_screen, input_text)
       #8 ========================================================================= PAUSE SCREEN ========================================================
       elif current_screen == "paused":
           if Initial_entry:
               selected_index = 0
               Initial_entry = False     
           selected_index, selected_option = handle_home_controls(selected_index, Paused_options, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option, previous_screen)
           render_pause(screen, Ubackground, Hfont, TITLE_font, HWIDTH,HHEIGHT,selected_index, Paused_options)
             
       #9 ========================================================================= LEVELS RENDERING =================================================================
       elif current_screen == "level_1":
            Initial_entry = True
            frame_counter += 1
            level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, game_time, holding_key, bombs, current_screen)
            all_blocks_positions = blocks_positions + Dblocks_positions1
            enemy_rect = create_enemy(enemy_x, enemy_y)
            enemy_rect2 = create_enemy(enemy2_x, enemy2_y)  # Coordinates for second enemy
            enemy_rect3 = create_enemy(enemy3_x, enemy3_y)
            player_position, current_screen, selected_option, previous_screen, is_moving, current_direction, bombs = handle_player_actions(Settings_options, current_screen, player_position, is_moving, current_direction, all_blocks_positions, bombs_list, enemy_rect, enemy_rect2, enemy_rect3)
            
            
            # Draw the enemy
            draw_enemies(screen, enemy_rect, Enemy_1_sprite )
            draw_enemies(screen, enemy_rect2, Enemy_1_sprite)
            draw_enemies(screen, enemy_rect3, Enemy_1_sprite)

            player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
            if (player_rect.colliderect(enemy_rect) or 
                player_rect.colliderect(enemy_rect2) or 
                player_rect.colliderect(enemy_rect3)) and not is_colliding_with_enemy:
                lives -= 1
                is_colliding_with_enemy = True  # Set the flag to True to indicate the player is currently colliding
                print(lives)
            elif not (player_rect.colliderect(enemy_rect) or 
                    player_rect.colliderect(enemy_rect2) or 
                    player_rect.colliderect(enemy_rect3)):
                is_colliding_with_enemy = False  # Reset the flag when the player is no longer colliding

            holding_key = draw_key(screen, holding_key, player_position, key_position1, key_position2, key_position3, current_screen, Key)
            selected_option, holding_key, player_position, rbombs = draw_door(screen, holding_key, player_position, door_position1, door_position2, door_position3, current_screen, doorway)

            draw_player(screen, player_position, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite, current_direction, is_moving, frame_counter)
            draw_blocks(screen, I_block, blocks_positions)

            draw_blocks(screen, D_block, Dblocks_positions1)  # create different patterns and change the sprites from level to level
            draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter)
            lives = handle_bomb_explosion(screen, bombs_list, Dblocks_positions1, player_position, lives)
            lives = handle_bomb_explosion(screen, bombs_list, blocks_positions, player_position, lives)
            if lives <= 0:
                selected_option = "DEATH"
            current_screen = handle_selected_option(selected_option, previous_screen)
       elif current_screen == "level_2":
            Initial_entry = True
            frame_counter += 1
            level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, game_time, holding_key, bombs, current_screen)
            all_blocks_positions = blocks_positions + Dblocks_positions2
            enemy_rect = create_enemy(enemy_x, enemy_y)
            enemy_rect2 = create_enemy(enemy2_x, enemy2_y)  # Coordinates for second enemy
            enemy_rect3 = create_enemy(enemy3_x, enemy3_y)
            player_position, current_screen, selected_option, previous_screen, is_moving, current_direction, bombs = handle_player_actions(Settings_options, current_screen, player_position, is_moving, current_direction, all_blocks_positions, bombs_list, enemy_rect, enemy_rect2, enemy_rect3)
            
            
            # Draw the enemy
            draw_enemies(screen, enemy_rect, Enemy_2_down_sprite )
            draw_enemies(screen, enemy_rect2, Enemy_2_down_sprite)
            draw_enemies(screen, enemy_rect3, Enemy_2_down_sprite)

            player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
            if (player_rect.colliderect(enemy_rect) or 
                player_rect.colliderect(enemy_rect2) or 
                player_rect.colliderect(enemy_rect3)) and not is_colliding_with_enemy:
                lives -= 1
                is_colliding_with_enemy = True  # Set the flag to True to indicate the player is currently colliding
                print(lives)
            elif not (player_rect.colliderect(enemy_rect) or 
                    player_rect.colliderect(enemy_rect2) or 
                    player_rect.colliderect(enemy_rect3)):
                is_colliding_with_enemy = False  # Reset the flag when the player is no longer colliding

            holding_key = draw_key(screen, holding_key, player_position, key_position1, key_position2, key_position3, current_screen, Key)
            selected_option, holding_key, player_position, rbombs = draw_door(screen, holding_key, player_position, door_position1, door_position2, door_position3, current_screen, doorway)

            draw_player(screen, player_position, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite, current_direction, is_moving, frame_counter)
            draw_blocks(screen, I_block, blocks_positions)

            draw_blocks(screen, D_block, Dblocks_positions2)  # create different patterns and change the sprites from level to level
            draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter)
            lives = handle_bomb_explosion(screen, bombs_list, Dblocks_positions2, player_position, lives)
            lives = handle_bomb_explosion(screen, bombs_list, blocks_positions, player_position, lives)
            if lives <= 0:
                selected_option = "DEATH"
            current_screen = handle_selected_option(selected_option, previous_screen)
       elif current_screen == "level_3":
            Initial_entry = True
            frame_counter += 1
            level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, game_time, holding_key, bombs, current_screen)
            all_blocks_positions = blocks_positions + Dblocks_positions3
            enemy_rect = create_enemy(enemy_x, enemy_y)
            enemy_rect2 = create_enemy(enemy2_x, enemy2_y)  # Coordinates for second enemy
            enemy_rect3 = create_enemy(enemy3_x, enemy3_y)
            player_position, current_screen, selected_option, previous_screen, is_moving, current_direction, bombs = handle_player_actions(Settings_options, current_screen, player_position, is_moving, current_direction, all_blocks_positions, bombs_list, enemy_rect, enemy_rect2, enemy_rect3)
            
            
            # Draw the enemy
            draw_enemies(screen, enemy_rect, Enemy_1_sprite )
            draw_enemies(screen, enemy_rect2, Enemy_2_down_sprite)
            draw_enemies(screen, enemy_rect3, Enemy_1_sprite)

            player_rect = pygame.Rect(player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE)
            if (player_rect.colliderect(enemy_rect) or 
                player_rect.colliderect(enemy_rect2) or 
                player_rect.colliderect(enemy_rect3)) and not is_colliding_with_enemy:
                lives -= 1
                is_colliding_with_enemy = True  # Set the flag to True to indicate the player is currently colliding
                print(lives)
            elif not (player_rect.colliderect(enemy_rect) or 
                    player_rect.colliderect(enemy_rect2) or 
                    player_rect.colliderect(enemy_rect3)):
                is_colliding_with_enemy = False  # Reset the flag when the player is no longer colliding

            holding_key = draw_key(screen, holding_key, player_position, key_position1, key_position2, key_position3, current_screen, Key)
            selected_option, holding_key, player_position, rbombs = draw_door(screen, holding_key, player_position, door_position1, door_position2, door_position3, current_screen, doorway)

            draw_player(screen, player_position, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite, current_direction, is_moving, frame_counter)
            draw_blocks(screen, I_block, blocks_positions)

            draw_blocks(screen, D_block, Dblocks_positions3)  # create different patterns and change the sprites from level to level
            draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter)
            lives = handle_bomb_explosion(screen, bombs_list, blocks_positions, player_position, lives)
            if lives <= 0:
                selected_option = "DEATH"
            current_screen = handle_selected_option(selected_option, previous_screen) 
       elif current_screen == "game_over":
           if Initial_entry:
               selected_index = 0
               Initial_entry = False   
           render_GameOver(screen, Hfont, Mbackground, Hbackground, HWIDTH, HHEIGHT)
           selected_index, selected_option = handle_home_controls(selected_index, End_options, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option, previous_screen)
       elif current_screen == "win":
           if Initial_entry:
               selected_index = 0
               Initial_entry = False   
               WINNER = selected_name
               W_points = points
           render_Win(screen, Hfont, Mbackground, Hbackground, HWIDTH, HHEIGHT)
           selected_index, selected_option = handle_home_controls(selected_index, End_options, Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option, previous_screen)
       #Update
       pygame.display.update()
       clock.tick(60)


if __name__ == "__main__":
   main()