from colors import *
from macro_actions import S

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'Code', # Application name
    'exec' : ['code','devenv'], # Executable names
    'logo' : 'code',
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (DIMBLUE, 'Over', [S("F10")]),
        (DIMBLUE, 'Into', [S("F11")]),
        (DIMBLUE, 'Out', [S("SHIFT", "F11")]),
        # 2nd row ----------
        (DIMGREEN, 'Debug', [S("F5")]),
        (DIMTEAL, 'Pause', [S("F6")]),
        (DIMRED, 'Stop', [S("SHIFT", "F5")]),
        # 3rd row ----------
        (TEAL, 'Breakpoint', [S("F9")]),
        (OFF, '', []),
        (OFF, '', []),
        # 4th row ----------
        (OFF, '', []),
        (OFF, '', []),
        (OFF, '', []),
        # Encoder button ---
        (OFF, '', [])
    ]
}
