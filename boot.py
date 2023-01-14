from board import *
from digitalio import DigitalInOut, Pull
import storage
import supervisor
import usb_cdc
import sys

btnUnlock = DigitalInOut(KEY1)
btnUnlock.pull = Pull.UP

if btnUnlock.value:     # BUTTON NOT PRESSED
    btnUnlock.deinit()
    print("Drive disabled")
    # storage.disable_usb_drive()
    if sys.implementation.version[0] == 8:
        supervisor.runtime.autoreload = False
    else:
        supervisor.disable_autoreload()
    print("Reload disabled")
    storage.remount("/", False)
    print("Enable USB Serial")
    usb_cdc.enable(console=True, data=True)    # Enable repl and serial
else:                   # BUTTON PRESSED
    btnUnlock.deinit()
    print("Drive enabled")
    if sys.implementation.version[0] == 8:
        supervisor.runtime.autoreload = False
    else:
        supervisor.disable_autoreload()
    print("Reload disabled")
    storage.remount("/", False)
    print("Enable USB Serial")
    usb_cdc.enable(console=True, data=True)    # Enable repl and serial
