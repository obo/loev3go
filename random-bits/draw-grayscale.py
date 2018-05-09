#!/usr/bin/env python3
# run me in ssh via:
#   brickrun ./draw-grayscale.py
# or
#   sudo openvt -s -w -- sudo --user robot -- ./draw-grayscale.py

from time import sleep

import ev3dev.auto as ev3

screen = ev3.Screen()

smile = True

while True:
    screen.clear()

    screen.draw.ellipse((20, 20, 60, 60))
    screen.draw.ellipse((30, 30, 50, 50), fill=128)
    screen.draw.ellipse((118, 20, 158, 60))
    screen.draw.ellipse((128, 30, 148, 50), fill=128)

    if smile:
        screen.draw.arc((20, 80, 158, 100), 0, 180)
    else:
        screen.draw.arc((20, 80, 158, 100), 180, 360)

    smile = not smile

    screen.update()

    sleep(1)
