#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

# 0 -128  ... means that no beacon is found
# 0 1     ... means that we are really really close
# 11 54   ... means that at "angle" 11, 54 "cm"

ir = ev3.InfraredSensor()
while True:
    print(ir.value(0), ir.value(1))
    time.sleep(1)
