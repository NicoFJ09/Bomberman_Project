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
    "DROP BOMB:": "SPACE",
    "DETONATE BOMB:": "F",
    "PAUSE:": "P",
    "SOUND TOGGLE:":"<-ON->", "MUSIC TOGGLE:":"<-ON->", "EXIT (APPLY CHANGES)":""
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
