import pygame
#Main structure
TITLE = "Bomberman"
RUNNING = True
#Screen dimensions
HWIDTH=1200
HHEIGHT=900

#Game section conditional
game_section= "intro"
prev_game_section = None
#Home screen
current_screen = "home"
selected_index = 0
selected_option = "MAIN MENU"
Home_options = ["START", "SETTINGS", "MANUAL", "TOP SCORES", "ABOUT"]
Home_screens = ["skin_select" , "name_select", "settings", "manual", "top_scores", "about", "home"]

#Settings screen
Settings_options = {
    "MOVE UP:": "W",
    "MOVE DOWN:": "S",
    "MOVE LEFT:": "A",
    "MOVE RIGHT:": "D",
    "DROP BOMB:": 'SPACE',
    "PAUSE:": "P",
    "RESTART:": "R",
    "SELECT:": 'RETURN', "MUSIC TOGGLE:":"<-ON->", "EXIT (APPLY CHANGES)":""
}

Paused_options =["RESUME", "SETTINGS", "MANUAL", "TOP SCORES", "ABOUT", "RESTART (A LIFE WILL BE LOST)", "MAIN MENU (DATA WILL BE LOST IF PRESSED)"]

MWIDTH=900 #MENU WIDTH
MHEIGHT=675 #MENU HEIGHT

#Blink selection
blink = False
blink_interval = 250  # Interval for blinking in milliseconds
last_blink_time = 0
selection_locked = False
next_value= None
Initial_entry = True

#Manual screens
pages=[1,2,3,4]
y_axis= "IMAGES"
PAGE_WIDTH = 675
PAGE_HEIGHT = 450

#User select
selected_skin_option = ""
selected_name = ""
input_text = ""

#Background music
music_playing = False

#LEVELS
Levels = ["Level 1", "Level 2", "Level 3"]

#==================================================MAIN GAME CONSTANTS ===============================================
player_position = [240,60]
PLAYER_SPEED = 5
PLAYER_SIZE=40
BLOCK_SIZE=60

points = 0
lives = 3
time = 0
holding_key= False
bombs= 10

num_frames_per_direction = 3
current_direction = "RIGHT"

is_moving= "FALSE"

frame_counter = 0

FRAME_DURATION= 10
