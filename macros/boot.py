# Alt Numpad for grub and BIOS
from colors import *
from macro_actions import S

app = {  # REQUIRED dict, must be named 'app'
    'name': 'grub',  # Application name
    # 'exec' : ['grub'], # Executable names
    'macros': [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (DIMYELLOW, 'Home', [S("HOME")]),
        (DIMYELLOW, 'Up', [S("UP_ARROW")]),
        (DIMYELLOW, 'PgUp', [S("PAGE_UP")]),
        # 2nd row ----------
        (DIMYELLOW, 'Left', [S("LEFT_ARROW")]),
        (DIMYELLOW, 'Enter', [S("ENTER")]),
        (DIMYELLOW, 'Right', [S("RIGHT_ARROW")]),
        # 3rd row ----------
        (DIMYELLOW, 'End', [S("END")]),
        (DIMYELLOW, 'Down', [S("DOWN_ARROW")]),
        (DIMYELLOW, 'PgDn', [S("PAGE_DOWN")]),
        # 4th row ----------
        (DIMWHITE, 'Del', [S("DELETE")]),
        (RED, 'F2', [S("F2")]),
        (DIMWHITE, 'Enter', [S("ENTER")]),
        # Encoder button ---
        (OFF, 'Esc', [S("ESCAPE")])
    ]
}
