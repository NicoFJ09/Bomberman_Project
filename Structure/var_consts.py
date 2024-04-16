import pygame
#Main structure
TITLE = "Bomberman"
RUNNING = True
#Screen dimensions
HWIDTH=1200
HHEIGHT=900

#Home screen
current_screen = "home"
selected_index = 0
selected_option = "MAIN MENU"
Home_options = ["START", "SETTINGS", "MANUAL", "TOP SCORES", "ABOUT"]


#Settings screen
Settings_options = {
    "MOVE UP:": "W",
    "MOVE DOWN:": "S",
    "MOVE LEFT:": "A",
    "MOVE RIGHT:": "D",
    "DROP BOMB:": ' ',
    "DETONATE BOMB:": "F",
    "PAUSE:": "P",
    "SELECT:": '\r',
    "SOUND TOGGLE:":"<-ON->", "MUSIC TOGGLE:":"<-ON->", "EXIT (APPLY CHANGES)":""
}

special_keys = {
    ' ': 'SPACE',
    '\r': 'RETURN',
    '\t' : 'TAB'
    # Add more special keys as needed
}

MWIDTH=900
MHEIGHT=675

#Blink selection
blink = False
blink_interval = 250  # Interval for blinking in milliseconds
last_blink_time = 0
selection_locked = False
next_value= None
Initial_entry = True
