#!/usr/bin/env python3
# from https://github.com/ev3dev/ev3dev-lang-python/issues/194

from time import sleep
import ev3dev.auto as ev3

screen = ev3.Screen()

smile = True

while True:
    screen.clear()

    # Screen.draw returns a PIL.ImageDraw handle
    screen.draw.ellipse(( 20, 20,  60, 60))
    screen.draw.ellipse((118, 20, 158, 60))

    if smile:
        screen.draw.arc((20, 80, 158, 100), 0, 180)
    else:
        screen.draw.arc((20, 80, 158, 100), 180, 360)

    smile = not smile

    # Update lcd display
    screen.update()

    sleep(1)
