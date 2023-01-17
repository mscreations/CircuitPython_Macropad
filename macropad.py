# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.

Uses code from following awesome projects:
https://github.com/Neradoc/Circuitpython_Hotkeys_Plus
and
https://github.com/xhargh/MacropadApplicationDetector
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from macro_actions import MacroAction, Tone, Type
from colors import *
import usb_cdc
import supervisor

# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'


# CLASSES AND FUNCTIONS ----------------

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences."""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self._logo = None
        if "logo" in appdata:
            self._logo = appdata["logo"]
        self._enter = None
        if "enter" in appdata and callable(appdata['enter']):
            self._enter = appdata['enter']
        self._leave = None
        if "leave" in appdata and callable(appdata['leave']):
            self._leave = appdata['leave']

        if 'exec' in appdata:
            self.exec = appdata['exec']
        else:
            self.exec = None

    def switch(self, prev_app=None):
        """ Activate application settings; update OLED labels and LED
            colors. """
        # the previous app's leave custom code
        if prev_app and prev_app._leave:
            prev_app._leave(pad=macropad, prev_app=prev_app, next_app=self)

        if self._logo:
            macropad.display_image("/images/" + self._logo + ".bmp")

        group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        if self._logo:
            time.sleep(0.2)
        macropad.display.show(group)
        macropad.display.refresh()

        if self._enter:
            self._enter(pad=macropad, prev_app=prev_app, next_app=self)

    def get_name(self):
        return self.name

    def get_exec(self):
        return self.exec

class SerialHandler:
    """
    Class for handling serial input from the connected computer
    """
    def __init__(self, in_buf_size=256):
        if usb_cdc.data is None:
            print("ERROR: Cannot enable data port. Is it enabled in boot.py?")
            return
        self.serial = usb_cdc.data
        self.in_data = bytearray()
        self.in_buf_size = in_buf_size
        print('Serial port initialized')

    def get_serial_input(self):
        if self.serial is None:
            macropad.red_led = False
            return
        if not self.serial.connected:
            macropad.red_led = False
            return
        macropad.red_led = True
        if self.serial.in_waiting > 0:
            b = self.serial.read(1)
            if b in [b'\n', b'\r']:
                # Echo back
                self.serial.write(b'Got: ')
                self.serial.write(self.in_data)
                self.serial.write(b'\r\n')
                # print(b)

                # Create string
                s = self.in_data.decode('utf-8')

                # TODO: Future improvement: add support for different kinds of data
                # ss = s.split(':', 1)

                # Reset in_data
                self.in_data = bytearray()
                return s
            else:
                if len(self.in_data) == self.in_buf_size:
                    self.serial.write(b'buf\n')
                    self.in_data = bytearray()

                self.in_data += b
                return None


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display_image("blinka.bmp")
time.sleep(2)

macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

serialHandler = SerialHandler()

def play_tone(note, duration):
    macropad.play_tone(note, duration)

Tone.play_tone = play_tone

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=FULLWHITE,
                            anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                            anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=FULLWHITE))
group.append(label.Label(terminalio.FONT, text='', color=BLACK,
                        anchored_position=(macropad.display.width//2, -2),
                        anchor_point=(0.5, 0.0)))
macropad.display.show(group)
macropad.group = group

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
boot_map = None
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            if filename == 'boot.py':
                # boot map, will be used as default until changed, then it will not be selectable
                # boot_map = App(module.app)
                pass
            else:
                # print(filename, len(apps))
                apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_position = None
prev_app_index = 0

if boot_map:
    # TODO: solve how to put boot app into a app_index that can be removed
    app_index = 0
    boot_map.switch()
    last_position = macropad.encoder
else:
    app_index = 0
    apps[app_index].switch()

shtdwn = False
disconnectCnt = 0       # Number of successive disconnects before powering down

# MAIN LOOP ----------------------------

while True:
        # Laptop power down handling
    if not supervisor.runtime.usb_connected:
        if disconnectCnt < 20:  # skip the first 20 disconnects
            disconnectCnt += 1  # in case the first are glitches
            continue
        shtdwn = True
        group.hidden = True
        macropad.pixels.brightness = 0.0
        macropad.display.refresh()
        macropad.pixels.show()
        disconnectCnt = 0
        continue
    if shtdwn:  # we will only reach here if we are no longer disconnected so turn back on
        disconnectCnt = 0
        group.hidden = False
        macropad.pixels.brightness = 1.0
        macropad.display.refresh()
        macropad.pixels.show()
        shtdwn = False

    # Read from serial port
    sin = serialHandler.get_serial_input()
    if sin:
        app_found = False
        for app in apps:
            if app.get_exec() and sin.lower() in app.get_exec():
                app.switch(apps[prev_app_index])
                app_index = apps.index(app)
                app_found = True
                break
        if not app_found:
            last_position = None

    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder
    if position != last_position:
        prev_app_index = app_index
        app_index = position % len(apps)
        apps[app_index].switch(apps[prev_app_index])
        last_position = position

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        if len(apps[app_index].macros) < 13:
            continue
        key_number = 12
        pressed = True
    elif macropad.encoder_switch_debounced.released:
        if len(apps[app_index].macros) < 13:
            continue
        key_number = 12
        pressed = False
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        if apps[app_index].macros[event.key_number][2] == '':
            continue # Key is blank in macro page or has no actions assigned. Skip.
        if apps[app_index].macros[event.key_number][1] == '':
            continue # Key disabled (no text). Skip.
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    sequence = apps[app_index].macros[key_number][2]
    if not isinstance(sequence, (list, tuple)):
        sequence = (sequence,)
    if pressed:
        # 'sequence' is arbitrary-length
        # each item in the sequence is either
        # an action instance or a floating point value
        # Action   ==>  execute the action
        # Float    ==>  sleep in seconds
        # Function ==>  call it with context
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = FULLWHITE
            macropad.pixels.show()
            group[key_number].color = BLACK
            group[key_number].background_color = FULLWHITE
            macropad.display.refresh()
        elif key_number == 12 and len(apps[app_index].macros[key_number][1]) > 0:
            for i in range(12):
                group[i].text = ''
            group[4].text = apps[app_index].macros[key_number][1]
            macropad.display.refresh()
        for index,item in enumerate(sequence):
            if item == 0:
                for item in sequence:
                    if isinstance(item, MacroAction):
                        item.release()
            elif isinstance(item, MacroAction):
                item.action()
            elif isinstance(item, float):
                time.sleep(item)
            elif callable(item):
                item(pad=macropad, key=key_number, idx=index)
            elif isinstance(item, int):
                # compatibility (legacy)
                if item > 0:
                    macropad.keyboard.press(item)
                else:
                    macropad.keyboard.release(item)
            elif isinstance(item, str):
                # compatibility (legacy)
                Type.write(item)
            else:
                print("Unknown action", item)
    else:
        # Release any still-pressed keys, consumer codes, mouse buttons
        for item in sequence:
            if isinstance(item, MacroAction):
                item.release()
            if isinstance(item, int) and item >= 0:
                macropad.keyboard.release(item)
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
            group[key_number].color = FULLWHITE
            group[key_number].background_color = None
            macropad.display.refresh()
        elif key_number == 12:
            for i in range(12):
                if i < len(apps[app_index].macros):
                    group[i].text = apps[app_index].macros[i][1]
                else:
                    group[i].text = ''
            macropad.display.refresh()
