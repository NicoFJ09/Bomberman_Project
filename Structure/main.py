# ============================================================= IMPORTS ===================================================================

import pygame
import sys
sys.path.append('../')
import os


#Home imports
from var_consts import *
from Screens.home import render_home
from Screens.settings import render_controls_volume
from Screens.manual import render_manual
from Screens.about import render_about
from Screens.top_scores import render_top_scores
from Screens.user_select import render_user_select

#Main game imports
from Player.controls import handle_player_actions, handle_bomb_explosion, create_enemy, move_enemy, check_enemy_collision, create_secondary_enemy, move_secondary_enemy, check_secondary_enemy_collision, handle_enemy_collision
from Player.display import draw_player, draw_blocks, draw_bombs, draw_enemy, draw_basic_enemy
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

#Level 2 Background
L2_bg = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Level2_bg.png").convert_alpha(), (900,780))
L3_bg = pygame.transform.scale(pygame.image.load("Assets/Backgrounds/Level3_bg.png").convert_alpha(), (900,780))
#Level 3 Background

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

#VICTORY SPRITES
S_win_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Sfrontal_2.png").convert_alpha(), (PAGE_WIDTH*(1/5),PAGE_HEIGHT*(4/9)))
B_win_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Bfrontal_2.png").convert_alpha(), (PAGE_WIDTH*(1/5),PAGE_HEIGHT*(4/9)))
K_win_sprite =  pygame.transform.scale(pygame.image.load("Assets/Sprites/Kfrontal_2.png").convert_alpha(), (PAGE_WIDTH*(2/9),PAGE_HEIGHT*(5/9)))
#DEATH SPRITES
S_lose_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Sdeath.png").convert_alpha(), (PAGE_WIDTH*(1/5),PAGE_HEIGHT*(4/9)))
B_lose_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Bdeath.png").convert_alpha(), (PAGE_WIDTH*(1/5),PAGE_HEIGHT*(4/9)))
K_lose_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Kdeath.png").convert_alpha(), (PAGE_WIDTH*(2/9),PAGE_HEIGHT*(1/3)))

skin_sprites = {
    "Samus": [Sfrontal_1, S_win_sprite, S_lose_sprite],  # List of Samus sprites
    "Bomberman": [Bfrontal_1, B_win_sprite, B_lose_sprite],  # List of Bomberman sprites
    "Kirby": [Kfrontal_1, K_win_sprite, K_lose_sprite]  # List of Kirby sprites
}
#Block sprites
D_block = pygame.transform.scale(pygame.image.load("Assets/Sprites/Destructable_block.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
D_block2 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Destructable_block_2.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
D_block3 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Destructable_block_3.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))

I_block = pygame.transform.scale(pygame.image.load("Assets/Sprites/Indestructable_block.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
I_block2 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Indestructable_block_2.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
I_block3 = pygame.transform.scale(pygame.image.load("Assets/Sprites/Indestructable_block_3.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
#Key sprite
Key = pygame.transform.scale(pygame.image.load("Assets/Sprites/Key.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
#DOORWAY
doorway = pygame.transform.scale(pygame.image.load("Assets/Sprites/closed_doorway.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
open_doorway = pygame.transform.scale(pygame.image.load("Assets/Sprites/doorway.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
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
Enemy_1_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_1_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
enemy_2_UP = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_2_up_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
enemy_2_DOWN = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_2_down_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
enemy_2_RIGHT = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_2_right_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
enemy_2_LEFT = pygame.transform.scale(pygame.image.load("Assets/Sprites/Enemy_2_left_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))


#BOMBS
Kbomb_load_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Kbomb_load_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
Bbomb_load_sprite = pygame.transform.scale(pygame.image.load("Assets/Sprites/Bbomb_load_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))
Sbomb_load_sprite =  pygame.transform.scale(pygame.image.load("Assets/Sprites/Sbomb_load_sprite.png").convert_alpha(), (BLOCK_SIZE*3,BLOCK_SIZE))

#EXPLOSION
Boom = pygame.transform.scale(pygame.image.load("Assets/Sprites/boom boom.png").convert_alpha(), (BLOCK_SIZE,BLOCK_SIZE))
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

# ====================================================== GAME TIMER UPDATE =================================================================
def update_timer(start_time):
    game_time = pygame.time.get_ticks() - start_time
    seconds = game_time // 1000
    minutes = seconds // 60
    seconds %= 60
    return minutes,seconds
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
                selected_option = "MAIN MENU (DATA WILL BE LOST IF PRESSED)"
                return selected_index, selected_option

   return handle_home_controls(selected_index, options, settings_options, selected_option)

# ================================================ SCREEN SELECTION HANDLING =============================================================================
def handle_selected_option(selected_option, previous_screen):
   global selection_locked, game_section, selected_skin_option, selected_name, input_text, player_position1, player_position2,player_position3, holding_key, bombs, lives,points, Dblocks_positions1, Dblocks_positions2, Dblocks_positions3, enemy, enemy2,enemy3, enemy_2, enemy2_2, enemy3_2, enemy_3, enemy2_3, enemy3_3, enemy4_3, ENEMY_SPEED
   if selected_option == "START":
       return "skin_select" 
   
   elif selected_option in skin_sprites and current_screen == "skin_select":
       return "name_select"
   
   elif selected_option == "name_select":
       return "name_select"
   
   elif selected_option == "change_level_1":
       player_position1 = [240,780]
       lives = 3
       bombs = 30
       holding_key = False
       Dblocks_positions1= [[(240, 480), (600, 480), (300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420), (360, 360), (600, 360), (960, 360), (240, 300), (300, 300), (420, 300), (960, 300), (900, 780), (960, 780), (1080, 780), (900, 60), (1080, 60), (480, 240), (600, 240), (720, 240), (1080, 240), (600, 720), (720, 720), (300, 180), (360, 180), (600, 180), (900, 180), (1080, 180), (360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660), (720, 600), (720, 540), (960, 540), (1080, 540)]]
       Dblocks_positions2= [[(1080, 420), (300, 60), (240, 600), (960, 240), (720, 720), (420, 180), (720, 240), (240, 300), (720, 540), (240, 360), (960, 300), (540, 420), (420, 660), (480, 60), (720, 780), (360, 420), (600, 720), (420, 300), (240, 480), (1080, 660), (600, 180), (720, 720), (840, 600), (660, 180), (1080, 180), (420, 300), (840, 360), (360, 540), (480, 240), (240, 300), (300, 420), (960, 420), (300, 180), (420, 180), (600, 180), (420, 780), (240, 480), (360, 180), (600, 480), (720, 660)]]
       Dblocks_positions3= [[(420, 420), (660, 420), (1080, 540), (1080, 180), (1080, 780), (240, 180), (840, 600), (1020, 60), (960, 600), (1020, 420), (600, 480), (600, 720), (600, 660), (900, 60), (840, 720), (360, 600), (960, 360), (360, 180), (240, 600), (360, 600)]]
       enemy = create_enemy(SPAWN_POSITIONS1_level_1)
       enemy2= create_enemy(SPAWN_POSITIONS2_level_1)
       enemy3 = create_enemy(SPAWN_POSITIONS3_level_1)
       ENEMY_SPEED = 2
       render_level_name(screen, Hfont, HWIDTH, HHEIGHT)
       return "level_1"
   elif selected_option == "change_level_2":
       player_position2 = [240,60]
       lives = 3
       bombs = 25
       holding_key = False
       Dblocks_positions1= [[(240, 480), (600, 480), (300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420), (360, 360), (600, 360), (960, 360), (240, 300), (300, 300), (420, 300), (960, 300), (900, 780), (960, 780), (1080, 780), (900, 60), (1080, 60), (480, 240), (600, 240), (720, 240), (1080, 240), (600, 720), (720, 720), (300, 180), (360, 180), (600, 180), (900, 180), (1080, 180), (360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660), (720, 600), (720, 540), (960, 540), (1080, 540)]]
       Dblocks_positions2= [[(1080, 420), (300, 60), (240, 600), (960, 240), (720, 720), (420, 180), (720, 240), (240, 300), (720, 540), (240, 360), (960, 300), (540, 420), (420, 660), (480, 60), (720, 780), (360, 420), (600, 720), (420, 300), (240, 480), (1080, 660), (600, 180), (720, 720), (840, 600), (660, 180), (1080, 180), (420, 300), (840, 360), (360, 540), (480, 240), (240, 300), (300, 420), (960, 420), (300, 180), (420, 180), (600, 180), (420, 780), (240, 480), (360, 180), (600, 480), (720, 660)]]
       Dblocks_positions3= [[(420, 420), (660, 420), (1080, 540), (1080, 180), (1080, 780), (240, 180), (840, 600), (1020, 60), (960, 600), (1020, 420), (600, 480), (600, 720), (600, 660), (900, 60), (840, 720), (360, 600), (960, 360), (360, 180), (240, 600), (360, 600)]]
       enemy_2 = create_enemy(SPAWN_POSITIONS1_level_2)
       enemy2_2= create_secondary_enemy(SPAWN_POSITIONS2_level_2)
       enemy3_2 = create_enemy(SPAWN_POSITIONS3_level_2)
       ENEMY_SPEED = 3
       render_level_name2(screen, Hfont, HWIDTH, HHEIGHT)
       return "level_2"
   elif selected_option == "change_level_3":
       player_position3 = [240,60]
       lives = 3
       bombs = 15
       holding_key = False
       Dblocks_positions1= [[(240, 480), (600, 480), (300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420), (360, 360), (600, 360), (960, 360), (240, 300), (300, 300), (420, 300), (960, 300), (900, 780), (960, 780), (1080, 780), (900, 60), (1080, 60), (480, 240), (600, 240), (720, 240), (1080, 240), (600, 720), (720, 720), (300, 180), (360, 180), (600, 180), (900, 180), (1080, 180), (360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660), (720, 600), (720, 540), (960, 540), (1080, 540)]]
       Dblocks_positions2= [[(1080, 420), (300, 60), (240, 600), (960, 240), (720, 720), (420, 180), (720, 240), (240, 300), (720, 540), (240, 360), (960, 300), (540, 420), (420, 660), (480, 60), (720, 780), (360, 420), (600, 720), (420, 300), (240, 480), (1080, 660), (600, 180), (720, 720), (840, 600), (660, 180), (1080, 180), (420, 300), (840, 360), (360, 540), (480, 240), (240, 300), (300, 420), (960, 420), (300, 180), (420, 180), (600, 180), (420, 780), (240, 480), (360, 180), (600, 480), (720, 660)]]
       Dblocks_positions3= [[(420, 420), (660, 420), (1080, 540), (1080, 180), (1080, 780), (240, 180), (840, 600), (1020, 60), (960, 600), (1020, 420), (600, 480), (600, 720), (600, 660), (900, 60), (840, 720), (360, 600), (960, 360), (360, 180), (240, 600), (360, 600)]]
       enemy_3 = create_enemy(SPAWN_POSITIONS1_level_3)
       enemy2_3= create_secondary_enemy(SPAWN_POSITIONS2_level_3)
       enemy3_3 = create_enemy(SPAWN_POSITIONS3_level_3)
       enemy4_3 = create_enemy(SPAWN_POSITIONS4_level_3)
       ENEMY_SPEED = 4
       render_level_name3(screen, Hfont, HWIDTH, HHEIGHT)
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
       game_section= "intro"
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
       player_position1 = [240,780]
       lives = 3
       bombs = 30
       points = 0
       holding_key = False
       Dblocks_positions1= [[(240, 480), (600, 480), (300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420), (360, 360), (600, 360), (960, 360), (240, 300), (300, 300), (420, 300), (960, 300), (900, 780), (960, 780), (1080, 780), (900, 60), (1080, 60), (480, 240), (600, 240), (720, 240), (1080, 240), (600, 720), (720, 720), (300, 180), (360, 180), (600, 180), (900, 180), (1080, 180), (360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660), (720, 600), (720, 540), (960, 540), (1080, 540)]]
       Dblocks_positions2= [[(1080, 420), (300, 60), (240, 600), (960, 240), (720, 720), (420, 180), (720, 240), (240, 300), (720, 540), (240, 360), (960, 300), (540, 420), (420, 660), (480, 60), (720, 780), (360, 420), (600, 720), (420, 300), (240, 480), (1080, 660), (600, 180), (720, 720), (840, 600), (660, 180), (1080, 180), (420, 300), (840, 360), (360, 540), (480, 240), (240, 300), (300, 420), (960, 420), (300, 180), (420, 180), (600, 180), (420, 780), (240, 480), (360, 180), (600, 480), (720, 660)]]
       Dblocks_positions3= [[(420, 420), (660, 420), (1080, 540), (1080, 180), (1080, 780), (240, 180), (840, 600), (1020, 60), (960, 600), (1020, 420), (600, 480), (600, 720), (600, 660), (900, 60), (840, 720), (360, 600), (960, 360), (360, 180), (240, 600), (360, 600)]]
       enemy = create_enemy(SPAWN_POSITIONS1_level_1)
       enemy2= create_enemy(SPAWN_POSITIONS2_level_1)
       enemy3 = create_enemy(SPAWN_POSITIONS3_level_1)
       return "level_1"
   elif selected_option == "DEATH":
       game_section= "intro"
       return "game_over"
   elif selected_option == "MAIN MENU (DATA WILL BE LOST IF PRESSED)":
       player_position1 = [240,780]
       lives = 3
       bombs = 30
       points= 0
       holding_key = False
       Dblocks_positions1= [[(240, 480), (600, 480), (300, 420), (360, 420), (660, 420), (900, 420), (960, 420), (1020, 420), (1080, 420), (360, 360), (600, 360), (960, 360), (240, 300), (300, 300), (420, 300), (960, 300), (900, 780), (960, 780), (1080, 780), (900, 60), (1080, 60), (480, 240), (600, 240), (720, 240), (1080, 240), (600, 720), (720, 720), (300, 180), (360, 180), (600, 180), (900, 180), (1080, 180), (360, 660), (420, 660), (540, 660), (780, 660), (780, 660), (1020, 660), (720, 600), (720, 540), (960, 540), (1080, 540)]]
       Dblocks_positions2= [[(1080, 420), (300, 60), (240, 600), (960, 240), (720, 720), (420, 180), (720, 240), (240, 300), (720, 540), (240, 360), (960, 300), (540, 420), (420, 660), (480, 60), (720, 780), (360, 420), (600, 720), (420, 300), (240, 480), (1080, 660), (600, 180), (720, 720), (840, 600), (660, 180), (1080, 180), (420, 300), (840, 360), (360, 540), (480, 240), (240, 300), (300, 420), (960, 420), (300, 180), (420, 180), (600, 180), (420, 780), (240, 480), (360, 180), (600, 480), (720, 660)]]
       Dblocks_positions3= [[(420, 420), (660, 420), (1080, 540), (1080, 180), (1080, 780), (240, 180), (840, 600), (1020, 60), (960, 600), (1020, 420), (600, 480), (600, 720), (600, 660), (900, 60), (840, 720), (360, 600), (960, 360), (360, 180), (240, 600), (360, 600)]]
       enemy = create_enemy(SPAWN_POSITIONS1_level_1)
       enemy2= create_enemy(SPAWN_POSITIONS2_level_1)
       enemy3 = create_enemy(SPAWN_POSITIONS3_level_1)
       selected_skin_option = ""
       selected_name = ""
       input_text = ""
       game_section= "intro"
       return "home"

#=========================================================================== ADD AND ORGANIZE FINAL SCORES ================================================================
def update_scores(scores, file_path):
    if not scores:  # Base case: If scores list is empty, do nothing
        return

    # Sort the scores in descending order of scores
    scores.sort(key=lambda x: x[1], reverse=True)

    # Write the sorted scores back to the file
    with open(file_path, 'w') as archivo:
        write_score(scores, archivo)

def write_score(scores, file_obj):
    if not scores:
        return
    name, score = scores.pop(0)
    file_obj.write(f"{name} : {score}\n")
    write_score(scores, file_obj)

def read_scores(file_path):
    scores = []

    def read_score_line(file_obj):
        line = file_obj.readline()
        if line:
            parts = line.strip().split(' : ')
            if len(parts) == 2:
                scores.append((parts[0], int(parts[1])))
            read_score_line(file_obj)

    try:
        with open(file_path, 'r') as archivo:
            read_score_line(archivo)
    except FileNotFoundError:
        pass  # No file found, scores list will be empty

    return scores

def score_append(score, name):
    # Get the directory of the current script file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create the file path relative to the directory of the current script file
    file_path = os.path.join(current_directory, 'scores.txt')

    # Read existing scores from the file
    scores = read_scores(file_path)

    # Append the new score and name
    scores.append((name, score))

    # Update scores in the file
    update_scores(scores, file_path)

# ========================================================================== MAIN CODE LOOP ==================================================================

def main():
   global selected_index, Settings_options,Levels, Home_options, selected_option, current_screen, blink, blink_interval, last_blink_time, Initial_entry, y_axis, selected_skin_option, selected_name, music_playing, player_position1,player_position2, player_position3, game_section, prev_game_section, current_direction, is_moving, frame_counter, holding_key, bombs, previous_screen, game_time, minutes, seconds, lives, WINNER, W_points, points, Dblocks_positions1, Dblocks_positions2, Dblocks_positions3, enemy, enemy2, enemy3, enemy_2, enemy2_2, enemy3_2, enemy_3, enemy2_3, enemy3_3, enemy4_3, collision_count, collision_state, ENEMY_SPEED
   while RUNNING:
       

       #Handle exit after pressing x
       handle_quit()
       if game_section != prev_game_section:
            prev_game_section = game_section
            music_playing = False  # Reset music_playing to False whenever game_section changes
            if game_section == "gameplay":
                start_time = pygame.time.get_ticks()  # Update start_time when gameplay section starts
        
       if game_section == "gameplay":
            minutes, seconds = update_timer(start_time)


        

       if Settings_options["MUSIC TOGGLE:"] == "<-ON->" or Settings_options["MUSIC TOGGLE:"] == "<-OFF->":
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
            ENEMY_SPEED = 2
            screen.fill((26, 140, 24))  # Green background
            Initial_entry = True
            frame_counter += 1
            level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, minutes, seconds, holding_key, bombs, current_screen)
            all_blocks_positions = blocks_positions + Dblocks_positions1
            player_position1, current_screen, selected_option, previous_screen, is_moving, current_direction, bombs = handle_player_actions(Settings_options, current_screen, player_position1, is_moving, current_direction, all_blocks_positions, bombs_list, bombs )
            enemy= move_secondary_enemy(enemy)
            enemy2= move_secondary_enemy(enemy2)
            enemy3= move_secondary_enemy(enemy3)
            check_secondary_enemy_collision(all_blocks_positions, enemy)
            check_secondary_enemy_collision (all_blocks_positions, enemy2)
            check_secondary_enemy_collision (all_blocks_positions, enemy3)
            holding_key = draw_key(screen, holding_key, player_position1, key_position1, key_position2, key_position3, current_screen, Key)
            selected_option, holding_key, player_position1 = draw_door(screen, holding_key, player_position1, door_position1, door_position2, door_position3, current_screen, doorway, open_doorway)

            draw_player(screen, player_position1, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite, current_direction, is_moving, frame_counter)
            draw_blocks(screen, I_block, blocks_positions)
            draw_blocks(screen, D_block, Dblocks_positions1)

            draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter)
            draw_basic_enemy(screen, enemy, frame_counter, Enemy_1_sprite)
            draw_basic_enemy(screen, enemy2, frame_counter, Enemy_1_sprite)
            draw_basic_enemy(screen, enemy3, frame_counter, Enemy_1_sprite)
            lives, Dblocks_positions1, points, enemy= handle_bomb_explosion(screen, bombs_list, Boom, player_position1, lives, Dblocks_positions1, points,enemy)
            lives, Dblocks_positions1, points, enemy2= handle_bomb_explosion(screen, bombs_list, Boom, player_position1, lives, Dblocks_positions1, points,enemy2 )
            lives, Dblocks_positions1, points, enemy3= handle_bomb_explosion(screen, bombs_list, Boom, player_position1, lives, Dblocks_positions1, points,enemy3 )
            lives, collision_state = handle_enemy_collision(player_position1, enemy, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position1, enemy2, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position1, enemy3, ENEMY_SIZE, lives)
            if lives <= 0:
                selected_option = "DEATH"
            current_screen = handle_selected_option(selected_option, previous_screen)
       elif current_screen == "level_2":
            ENEMY_SPEED = 3
            screen.blit(L2_bg, (240, 60))
            Initial_entry = True
            frame_counter += 1
            level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, minutes, seconds, holding_key, bombs, current_screen)
            all_blocks_positions = blocks_positions + Dblocks_positions2
            player_position2, current_screen, selected_option, previous_screen, is_moving, current_direction, bombs = handle_player_actions(Settings_options, current_screen, player_position2, is_moving, current_direction, all_blocks_positions, bombs_list, bombs )
            enemy_2= move_enemy(enemy_2)
            enemy2_2= move_secondary_enemy(enemy2_2)
            enemy3_2= move_enemy(enemy3_2)
            check_enemy_collision(all_blocks_positions, enemy_2)
            check_secondary_enemy_collision (all_blocks_positions, enemy2_2)
            check_enemy_collision(all_blocks_positions, enemy3_2)
            holding_key = draw_key(screen, holding_key, player_position2, key_position1, key_position2, key_position3, current_screen, Key)
            selected_option, holding_key, player_position2 = draw_door(screen, holding_key, player_position2, door_position1, door_position2, door_position3, current_screen, doorway, open_doorway)

            draw_player(screen, player_position2, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite, current_direction, is_moving, frame_counter)
            draw_blocks(screen, I_block2, blocks_positions)
            draw_blocks(screen, D_block2, Dblocks_positions2)

            draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter)
            draw_enemy(screen, enemy_2, frame_counter, enemy_2_UP, enemy_2_DOWN,enemy_2_RIGHT, enemy_2_LEFT)
            draw_basic_enemy(screen, enemy2_2, frame_counter, Enemy_1_sprite)
            draw_enemy(screen, enemy3_2, frame_counter, enemy_2_UP, enemy_2_DOWN,enemy_2_RIGHT, enemy_2_LEFT)
            lives, Dblocks_positions2, points, enemy_2= handle_bomb_explosion(screen, bombs_list, Boom, player_position2, lives, Dblocks_positions2, points,enemy_2 )
            lives, Dblocks_positions2, points, enemy2_2= handle_bomb_explosion(screen, bombs_list, Boom, player_position2, lives, Dblocks_positions2, points,enemy2_2 )
            lives, Dblocks_positions2, points, enemy3_2= handle_bomb_explosion(screen, bombs_list, Boom, player_position2, lives, Dblocks_positions2, points,enemy3_2 )
            lives, collision_state = handle_enemy_collision(player_position2, enemy_2, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position2, enemy2_2, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position2, enemy3_2, ENEMY_SIZE, lives)
            if lives <= 0:
                selected_option = "DEATH"
            current_screen = handle_selected_option(selected_option, previous_screen)
       elif current_screen == "level_3":
            screen.blit(L3_bg, (240, 60))
            Initial_entry = True
            frame_counter += 1
            level_constants(screen, GAME_font, HWIDTH, HHEIGHT, points, lives, minutes, seconds, holding_key, bombs, current_screen)
            all_blocks_positions = blocks_positions + Dblocks_positions3
            player_position3, current_screen, selected_option, previous_screen, is_moving, current_direction, bombs = handle_player_actions(Settings_options, current_screen, player_position3, is_moving, current_direction, all_blocks_positions, bombs_list, bombs)
            ENEMY_SPEED = 4
            enemy_3= move_enemy(enemy_3)
            enemy2_3= move_secondary_enemy(enemy2_3)
            enemy3_3= move_enemy(enemy3_3)
            enemy4_3= move_enemy(enemy4_3)
            check_enemy_collision(all_blocks_positions, enemy_3)
            check_secondary_enemy_collision (all_blocks_positions, enemy2_3)
            check_enemy_collision(all_blocks_positions, enemy3_3)
            check_enemy_collision(all_blocks_positions, enemy4_3)
            holding_key = draw_key(screen, holding_key, player_position3, key_position1, key_position2, key_position3, current_screen, Key)
            selected_option, holding_key, player_position3 = draw_door(screen, holding_key, player_position3, door_position1, door_position2, door_position3, current_screen, doorway, open_doorway)

            draw_player(screen, player_position3, selected_skin_option, B_up_sprite, B_down_sprite, B_left_sprite, B_right_sprite, K_up_sprite, K_down_sprite, K_left_sprite, K_right_sprite, S_left_sprite, S_right_sprite, current_direction, is_moving, frame_counter)
            draw_blocks(screen, I_block3, blocks_positions)
            draw_blocks(screen, D_block3, Dblocks_positions3)

            draw_bombs(screen, selected_skin_option, bombs_list, Kbomb_load_sprite, Bbomb_load_sprite, Sbomb_load_sprite, frame_counter)
            draw_enemy(screen, enemy_3, frame_counter, enemy_2_UP, enemy_2_DOWN,enemy_2_RIGHT, enemy_2_LEFT)
            draw_basic_enemy(screen, enemy2_3, frame_counter, Enemy_1_sprite)
            draw_enemy(screen, enemy3_3, frame_counter, enemy_2_UP, enemy_2_DOWN,enemy_2_RIGHT, enemy_2_LEFT)
            draw_enemy(screen, enemy4_3, frame_counter, enemy_2_UP, enemy_2_DOWN,enemy_2_RIGHT, enemy_2_LEFT)
            lives, Dblocks_positions3, points, enemy_3= handle_bomb_explosion(screen, bombs_list, Boom, player_position3, lives, Dblocks_positions3, points,enemy_3 )
            lives, Dblocks_positions3, points, enemy2_3= handle_bomb_explosion(screen, bombs_list, Boom, player_position3, lives, Dblocks_positions3, points,enemy2_3 )
            lives, Dblocks_positions3, points, enemy3_3= handle_bomb_explosion(screen, bombs_list, Boom, player_position3, lives, Dblocks_positions3, points,enemy3_3 )
            lives, Dblocks_positions3, points, enemy4_3= handle_bomb_explosion(screen, bombs_list, Boom, player_position3, lives, Dblocks_positions3, points,enemy4_3 )
            lives, collision_state = handle_enemy_collision(player_position3, enemy_3, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position3, enemy2_3, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position3, enemy3_3, ENEMY_SIZE, lives)
            lives, collision_state = handle_enemy_collision(player_position3, enemy4_3, ENEMY_SIZE, lives)
            if lives <= 0:
                selected_option = "DEATH"
            current_screen = handle_selected_option(selected_option, previous_screen) 
       elif current_screen == "game_over":
           if Initial_entry:
               selected_index = 0
               Initial_entry = False   
               skin_lose = selected_skin_option
            
           render_GameOver(screen, Hfont, Mbackground, Hbackground, HWIDTH, HHEIGHT, skin_sprites,skin_lose)
           selected_index, selected_option = handle_home_controls(selected_index, ["MAIN MENU (DATA WILL BE LOST IF PRESSED)"], Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option, previous_screen)
       elif current_screen == "win":
           if Initial_entry:
               selected_index = 0
               Initial_entry = False   
               WINNER = selected_name
               skin_win = selected_skin_option
               W_points = points
               Fminutes, Fseconds=minutes, seconds
               score_append(W_points, WINNER)
           render_Win(screen, Hfont, Mbackground, Hbackground, HWIDTH, HHEIGHT, skin_sprites,skin_win, W_points,Fminutes, Fseconds)
           selected_index, selected_option = handle_home_controls(selected_index, ["MAIN MENU (DATA WILL BE LOST IF PRESSED)"], Settings_options, selected_option)
           current_screen = handle_selected_option(selected_option, previous_screen)
           
       #Update
       pygame.display.update()
       clock.tick(60)


if __name__ == "__main__":
   main()