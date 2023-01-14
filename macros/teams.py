from colors import *
from macro_actions import S, C

# This maps features to Fkeys which AutoHotKey then brings
# the window to focus and presses the correct key sequence

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'Teams', # Application name
    'exec' : ['teams.exe'], # Executable names
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (GREEN, 'Accept', [S("F16")]),
        (PURPLE, 'Hand', [S("F21")]),
        (RED, 'Leave', [S("F19")]),
        # 2nd row ----------
        (OFF, '', []),
        (RED, 'ScreenShare', [S("F20")]),
        (OFF, '', []),
        # 3rd row ----------
        (DIMRED, 'VolMute', [C("MUTE")]),
        (OFF, '', []),
        (RED, 'MicMute', [S("F14")]),
        # 4th row ----------
        (GREEN, 'Join', [S("F18")]),
        (GREEN, 'Cam', [S("F15")]),
        (RED, 'Decline', [S("F17")]),
        # Encoder button ---
        (OFF, '', [])
    ]
}
# f16 accept video call
# f17 decline call
# f18 join meeting
