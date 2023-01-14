# MACROPAD Teams
from macro_actions import S
from colors import *

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Function Keys', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (DIMBLUE, 'F14', S("F14")),
        (DIMBLUE, 'F15', S("F15")),
        (DIMBLUE, 'F16', S("F16")),
        # 2nd row ----------
        (DIMBLUE, 'F17', S("F17")),
        (DIMBLUE, 'F18', S("F18")),
        (DIMBLUE, 'F19', S("F19")),
        # 3rd row ----------
        (DIMBLUE, 'F20', S("F20")),
        (DIMBLUE, 'F21', S("F21")),
        (DIMBLUE, 'F22', S("F22")),
        # 4th row ----------
        (DIMBLUE, 'F23', S("F23")),
        (DIMBLUE, 'F24', S("F24")),
        (OFF, '', ''),
        # Encoder button ---
        (OFF, '', '')
    ]
}
