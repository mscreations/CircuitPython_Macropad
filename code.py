import microcontroller
import sys

try:
    print("Starting macropad")
    import macropad
except Exception as e:
    import time
    import traceback
    error = traceback.format_exception(e, e, e.__traceback__)
    if sys.implementation.version[0] == 8:
        error = "\r\n".join(error).split().replace("\r\n", " | ")
    else:
        error = error.strip().replace("\r\n", " | ")

    while True:
        print("\n----------")
        for word in error.split(" "):
            print(word, end=" ")
            time.sleep(0.5)
        time.sleep(1)
        microcontroller.reset()
