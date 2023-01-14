"""
Setup the Keycode and Layout modules to use in the macros.
default_layout = ...
default_keycode = ...
"""
# from keyboard_layout_mac_fr import KeyboardLayout
# default_layout = KeyboardLayout
# from keycode_mac_fr import Keycode
# default_keycode = Keycode

# Suppress exceptions from serial by setting the default layout and keycodes
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
default_layout = KeyboardLayoutUS

from adafruit_hid.keycode import Keycode
default_keycode = Keycode