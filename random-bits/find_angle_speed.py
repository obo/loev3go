#!/usr/bin/env python3
# dbg print
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from ev3dev.auto import *

import random


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x

class Test:
    def __init__(self):
        self.left_motor=LargeMotor(OUTPUT_B)
        self.right_motor=LargeMotor(OUTPUT_C)
        self.polarity = -1
        self.speed = 100 # rotation speed of each of the motors

    def __del__(self):
        self.left_motor.stop()
        self.right_motor.stop()
        
    def calibrate_angle(self):
        ir = InfraredSensor(); assert ir.connected
        ir.mode = "IR-SEEK"
        startlpos = self.left_motor.position
        startrpos = self.right_motor.position
        lastlpos = startlpos
        lastrpos = startrpos
        reported = 0
        while True:
            # print(ir.value(0), ir.value(1))
            if ir.value(1) == -128:
              print("Beacon lost, waiting")
              self.left_motor.stop(stop_action="hold")
              self.right_motor.stop()
              time.sleep(1)
            else:
              # Rotating to face the beacon
              self.left_motor.run_forever(speed_sp=self.speed)
              self.right_motor.run_forever(speed_sp=(-1.0)*self.speed)
              irangle = ir.value(0)
              lpos = self.left_motor.position
              rpos = self.right_motor.position
              # print("A:", irangle, ", L:", lpos, ", R:", rpos)
              if irangle == 0:
                ldiff = abs(lpos -lastlpos)
                if ldiff > 400:
                  if reported > 0:
                    print("At", self.speed, ", travel for 1/2circ ", ldiff, "L and", abs(rpos-lastrpos), "R; absL:", abs(lpos-startlpos), ", absR:", abs(rpos-startrpos))
                  lastlpos = lpos
                  lastrpos = rpos
                  if reported > 4:
                    self.speed=60+30*random.randint(1,4)
                    if random.randint(0,1)==1:
                      self.speed*= -1
                    reported = 0
                  reported += 1

o=Test()
o.calibrate_angle()



