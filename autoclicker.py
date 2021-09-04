#######################
# Script by Forestcat #
#######################

"""
This a very small autoclicker, just for fun use.
It uses the pynput library, you can easy install
by typing "pip3 install pynput"
By default the time between the click and the release is 0.01 seconds, but you can change if you wish.
If you want a right click then change Button.left on line 39 and 41 to Button.right or Button.middle
Have fun and enjoy!
"""

from pynput.mouse import Button, Controller 
from pynput import keyboard
import threading, time

mouse = Controller()
loop = False
running = True

def on_press(key):
    global loop
    if key == keyboard.Key.f8 and loop == False:
        loop = True
    elif key == keyboard.Key.f8 and loop == True:
        loop = False
    elif key == keyboard.Key.f9:
        global running
        loop = False
        running = False
        return False
        
listener = keyboard.Listener(on_press=on_press)
listener.start()

while running:
    while loop:
        mouse.press(Button.left)
        time.sleep(0.01)
        mouse.release(Button.left)
        
