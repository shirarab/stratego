import tkinter as tk

OUTLINE_BOARD_FRAME_SIZE = 450
BOARD_FRAME_SIZE = 450
SOLDIERS_FRAME_SIZE = 90
TITLE_FRAME_SIZE = 30
OUTLINE_SOLDIERS_FRAME_WIDTH = 410
OUTLINE_SOLDIERS_FRAME_HEIGHT = BOARD_FRAME_SIZE
SOLDIERS_BOARD_WIDTH = 380
SOLDIERS_BOARD_HEIGHT = 220
GREEN = 'green'
LIGHT_GRAY = 'light gray'

# # Frames:
OUTLINE_SOLDIERS_FRAME_STYLE = {'bg': LIGHT_GRAY,
                                'highlightbackground': LIGHT_GRAY, 'highlightcolor': LIGHT_GRAY,
                                'width': OUTLINE_SOLDIERS_FRAME_WIDTH,
                                'height': OUTLINE_SOLDIERS_FRAME_HEIGHT}
OUTLINE_BOARD_FRAME_STYLE = {'bg': GREEN,
                             'padx': 50,
                             'pady': 10}
OUTLINE_RED_FRAME_STYLE = {'bg': LIGHT_GRAY,
                           'width': SOLDIERS_BOARD_WIDTH,
                           'height': SOLDIERS_BOARD_HEIGHT}
OUTLINE_BLUE_FRAME_STYLE = {'bg': LIGHT_GRAY,
                            'width': SOLDIERS_BOARD_WIDTH,
                            'height': SOLDIERS_BOARD_HEIGHT}

NORMAL_BG = {'bg': LIGHT_GRAY}
MENU_BG = {'bg': 'RoyalBlue1', 'bd': 5}
MAIN_STYLE = {'highlightbackground': 'light gray', 'highlightthickness': 2, **NORMAL_BG}

BASIC_SOLDIER_STYLE = {
    'font': ('Courier', 20),
    'fg': LIGHT_GRAY,
    'width': 2,
    # 'height': 2
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
                     'bg': 'gray',
                     'anchor': tk.CENTER,
                     'bd': 10,
                     'fg': 'white'}
