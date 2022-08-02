import tkinter as tk

OUTLINE_BOARD_FRAME_SIZE = 450
BOARD_FRAME_SIZE = 450
SOLDIERS_FRAME_SIZE = 90
TITLE_FRAME_SIZE = 30
OUTLINE_SOLDIERS_FRAME_WIDTH = 410
OUTLINE_SOLDIERS_FRAME_HEIGHT = BOARD_FRAME_SIZE
SOLDIERS_BOARD_WIDTH = 380
SOLDIERS_BOARD_HEIGHT = 220

# # Frames:
OUTLINE_SOLDIERS_FRAME_STYLE = {'bg': 'gray',
                                'width': OUTLINE_SOLDIERS_FRAME_WIDTH,
                                'height': OUTLINE_SOLDIERS_FRAME_HEIGHT}
OUTLINE_BOARD_FRAME_STYLE = {'bg': 'green',
                             'padx': 50,
                             'pady': 10}
OUTLINE_RED_FRAME_STYLE = {'bg': 'orange',
                           'width': SOLDIERS_BOARD_WIDTH,
                           'height': SOLDIERS_BOARD_HEIGHT}
OUTLINE_BLUE_FRAME_STYLE = {'bg': 'yellow',
                            'width': SOLDIERS_BOARD_WIDTH,
                            'height': SOLDIERS_BOARD_HEIGHT}

NORMAL_BG = {'bg': 'white'}
MENU_BG = {'bg': 'RoyalBlue1', 'bd': 5}
MAIN_STYLE = {'highlightbackground': 'deep pink', 'highlightthickness': 2, **NORMAL_BG}

BASIC_SOLDIER_STYLE = {
    'font': ('Courier', 20),
    'fg': 'white'
}

EMPTY_SOLDIER_STYLE = {
    'bg': 'gold',
    **BASIC_SOLDIER_STYLE
}

WATER_SOLDIER_STYLE = {
    'bg': 'DeepSkyBlue2',
    **BASIC_SOLDIER_STYLE
}

BLUE_SOLDIER_STYLE = {
    'bg': 'navy',
    **BASIC_SOLDIER_STYLE
}

RED_SOLDIER_STYLE = {
    'bg': 'red4',
    **BASIC_SOLDIER_STYLE
}

TITLE_LABEL_STYLE = {'font': ('Comic Sans MS', 15),
                     'relief': tk.GROOVE,
                     'bg': 'thistle1',
                     'anchor': tk.CENTER,
                     'bd': 10,
                     'fg': 'deep pink'}

# HIGH_BG = {'bg': 'midnight blue'}
# SUB_STYLE = {'highlightthickness': 1,
#              **NORMAL_BG}
# BOARD_BG = {'bg': 'lavender'}
#
# # board cells (buttons):
# NORMAL_BTN = {'bg': 'MediumPurple2',
#               'fg': 'white'}
# DIS_BTN = {'bg': 'thistle3', 'fg': 'gray75'}
# PRESSED_BTN = {'activebackground': 'plum1',
#                'activeforeground': 'plum4'}
# BTN_STYLE = {'font': ('Courier', 20),
#              **NORMAL_BTN,
#              'width': 3,
#              'height': 3}

# # widgets:
# MSG_STL = {'font': ('Courier', 12), 'fg': 'gray6', **NORMAL_BG}
# WORDS_STYLE = {'font': ('Tempus Sans ITC', 12), }
# TXT_STYLE = {'font': ('Tempus Sans ITC', 15)}
# TITLE_TXT = {'font': ("Comic Sans MS", 10), 'fg': 'white', 'width': 11}
# TITLE_STYLE = {**TITLE_TXT, **MENU_BG}
# HIGH_STYLE = {**TITLE_TXT, **HIGH_BG}
# WORDS_TITLE_STL = {'font': ("Comic Sans MS", 15), 'pady': 5,
#                    'relief': tk.GROOVE}
# ENTER_STL = {'font': ("Comic Sans MS", 15),
#              'bg': 'lavender',
#              'fg': 'MediumPurple4',
#              **PRESSED_BTN}
#
# MENU_BTN_GRID = {'sticky': tk.NSEW,
#                  'padx': 2, 'pady': 2}
#
# # the chosen word:
# CH_WORD_STL = {'font': ('Tempus Sans ITC', 15)}
# CH_WORD_BG = {'bg': 'thistle1'}
#
# # placing:
# CENTER = {'relx': 0.5, 'rely': 0.5, 'anchor': tk.CENTER}
# CENTER_UP = {'relx': 0.5, 'rely': 0.3, 'anchor': tk.CENTER}
# CENTER_DOWN = {'relx': 0.5, 'rely': 0.75, 'anchor': tk.CENTER}
