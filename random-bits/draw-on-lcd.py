#!/usr/bin/env python
# from http://www.ev3dev.org/docs/tutorials/using-ev3-lcd/
# When remote-controlling, run using:
#  sudo openvt -s -w -- sudo --user robot -- ./draw-on-lcd.py

# Hard coding these values is not a good idea because the values could
# change. But, since this is an example, we want to keep it short.
SCREEN_WIDTH = 178 # pixels
SCREEN_HEIGHT = 128 # pixels
LINE_LENGTH = 24 # bytes
SIZE = 3072 # bytes

import os
import array
from time import sleep


def main():
    buf = [0] * SIZE

    # draw a vertical line in column 100 (0 based index)
    for row in range(0, SCREEN_HEIGHT):
        buf[row * LINE_LENGTH + int(100 / 8)] = 1 << (100 % 8)

    # draw a horizontal line in row 64 (0 based index)
    for col in range(0, LINE_LENGTH):
        buf[64 * LINE_LENGTH + col] = 0xff


    import math
    # draw a circle, center at (40,40), radius is 20
    for x in range(0, 20):
        y = math.sqrt(20 * 20 - x * x)
        buf[(40 + int(y)) * LINE_LENGTH + int((40 + x) / 8)] = 1 << ((40 + x) % 8)
        buf[(40 - int(y)) * LINE_LENGTH + int((40 + x) / 8)] = 1 << ((40 + x) % 8)
        buf[(40 + int(y)) * LINE_LENGTH + int((40 - x) / 8)] = 1 << ((40 - x) % 8)
        buf[(40 - int(y)) * LINE_LENGTH + int((40 - x) / 8)] = 1 << ((40 - x) % 8)

    f = os.open('/dev/fb0', os.O_RDWR)
    s = array.array('B', buf).tostring()
    os.write(f, s)
    print("Written. Sleeping")
    sleep(3)
    os.close(f)

if __name__ == '__main__':
    main()
    print("Closed. Sleeping")
    sleep(3)

