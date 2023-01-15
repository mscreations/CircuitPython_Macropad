# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Universal Numpad

from colors import *
from macro_actions import S

app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Numpad', # Application name
    'exec' : ['excel', 'speedcrunch', 'calculatorapp', 'calculator', 'calc'], # Executable names
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (DIMYELLOW, '7', [S('7')]),
        (DIMYELLOW, '8', [S('8')]),
        (DIMYELLOW, '9', [S('9')]),
        # 2nd row ----------
        (DIMYELLOW, '4', [S('4')]),
        (DIMYELLOW, '5', [S('5')]),
        (DIMYELLOW, '6', [S('6')]),
        # 3rd row ----------
        (DIMYELLOW, '1', [S('1')]),
        (DIMYELLOW, '2', [S('2')]),
        (DIMYELLOW, '3', [S('3')]),
        # 4th row ----------
        (DIMWHITE, '*', [S('*')]),
        (RED, '0', [S('0')]),
        (DIMWHITE, '#', [S('#')]),
        # Encoder button ---
        (OFF, '', [S("BACKSPACE")])
    ]
}
