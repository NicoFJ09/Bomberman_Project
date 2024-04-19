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
    "PAUSE:": "P",
    "RESTART": "R",
    "SELECT:": '\r',
    "SOUND TOGGLE:":"<-ON->", "MUSIC TOGGLE:":"<-ON->", "EXIT (APPLY CHANGES)":""
}

special_keys = {
    ' ': 'SPACE',
    '\r': 'RETURN',
    '\t' : 'TAB',
    '^[': 'ESCAPE',
    '!': 'EXCLAIM',
    '"': 'QUOTEDBL',
    '#': 'HASH',
    '$': 'DOLLAR',
    '&': 'AMPERSAND',
    '\'': 'QUOTE',
    '(': 'LEFTPAREN',
    ')': 'RIGHTPAREN',
    '*': 'ASTERISK',
    '+': 'PLUS',
    ',': 'COMMA',
    '-': 'MINUS',
    '.': 'PERIOD',
    '/': 'SLASH',
    ':': 'COLON',
    ';': 'SEMICOLON',
    '<': 'LESS',
    '=': 'EQUALS',
    '>': 'GREATER',
    '?': 'QUESTION',
    '@': 'AT',
    '[': 'LEFTBRACKET',
    '\\': 'BACKSLASH',
    ']': 'RIGHTBRACKET',
    '^': 'CARET',
    '_': 'UNDERSCORE',
    '`': 'BACKQUOTE',
    '^[A': 'LEFTARROW',
    '^[[B': 'DOWNARROW',
    '^[[C': 'RIGHTARROW',
    '^[[D': 'UPARROW',
    '^[[E': 'INSERT',
    '^[[F': 'HOME',
    '^[[H': 'END',
    '^[[5~': 'PAGEUP',
    '^[[6~': 'PAGEDOWN',
    '^[[1~': 'F1',
    '^[[2~': 'F2',
    '^[[3~': 'F3',
    '^[[4~': 'F4',
    '^[[5~': 'F5',
    '^[[6~': 'F6',
    '^[[7~': 'F7',
    '^[[8~': 'F8',
    '^[[9~': 'F9',
    '^[[10~': 'F10',
    '^[[11~': 'F11',
    '^[[12~': 'F12',
    '^[[13~': 'F13',
    '^[[14~': 'F14',
    '^[[15~': 'F15',
    '^[[?2~': 'NUMLOCK',
    '^[[?1~': 'CAPSLOCK',
    '^[[?3~': 'SCROLLOCK',
    '^[[1~': 'LSHIFT',
    '^[[2~': 'RSHIFT',
    '^[[3~': 'LCTRL',
    '^[[4~': 'RCTRL',
    '^[[5~': 'LALT',
    '^[[6~': 'RALT',
    '^[[7~': 'LMETA',
    '^[[8~': 'RMETA',
    '^[[9~': 'LWINDOWS',
    '^[[10~': 'RWINDOWS',
    '^[[11~': 'MODE',
    '^[[12~': 'HELP',
    '^[[13~': 'PRINT',
    '^[[14~': 'SYSREQ',
    '^[[15~': 'BREAK',
    '^[[16~': 'MENU',
    '^[[17~': 'POWER',
    '^[[18~': 'EURO',
    '^[[19~': 'UNDO',
    '^[[20~': 'ANDROIDBACK'
}

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

#Skin select
skins= ["Samus", "Bomberman", "Kirby"]