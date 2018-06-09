# EV3 Logo, Drawing on the ground with a turtle robot

# dbg print
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from time   import time, sleep
from ev3dev.auto import *

from src.PenSelector import *

# Connect two large motors on output ports B and C and check that
# the device is connected using the 'connected' property.
#print('Connecting motors')
left_motor = LargeMotor(OUTPUT_B);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C); assert right_motor.connected
polarity = -1
  # polarity means where the 'head' of the robot is wrt to motor direction

speed = 300 # rotation speed of each of the motors
moving_speed = 30 # how many tacho counts is one unit of "forward"
angle_speed = 2098/360
  # how much have both left and right motor roll (in opposite directions)
  # to get 1 degree of overall rotation

# for simplicity, we include polarity in moving speed
moving_speed *= polarity


# # automatic stopping when this unit is destroyed
# import weakref
# class Ev3_Turtle_Object:
#   pass
# alive=Ev3_Turtle_Object()
# def finalizer:
#   left_motor.stop()
#   right_motor.stop()
# weakref.finalize(alive, finalizer)


import turtle
import math
import weakref
import threading
import sys

from pylogo.common import *

eprint("ev3_turtle starting")

class Turtle:

    _all_turtles = []
    _turtle_count = 1

    def __init__(self, use_turtle = turtle):
        eprint("init")
        global left_motor
        global right_motor
        global speed
        global moving_speed
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.speed = speed
        self.moving_speed = moving_speed
        self.angle_speed = angle_speed
        self.pen_down = False
        # assume we start with the pen up
        self.pen_color = LEFT_PEN
        ## The following is from ps_turtle, trying to avoid
        ## ps_turtle and ev3_turtle's interpreters fight over tk
        self.pen = use_turtle # use plain turtle graphics
        self.pen.degrees()
        turtle.tracer(False) # this affects the *global* turtle, not use_turtle
        turtle.ht() # this affects the *global* turtle, not use_turtle
        self.pen.speed(0)
        # self.pen = turtle.RawPen(get_canvas())
        # self.pen.degrees()
        # self._all_turtles.append(weakref.ref(self))
        # self._count = self._turtle_count
        # self.__class__._turtle_count += 1

    def __repr__(self):
        return '<%s %i>' % (self.__class__.__name__,
                            self._count)
    def __del__(self):
        global left_motor
        global right_motor
        left_motor.stop()
        right_motor.stop()

    @logofunc()
    def turtle(self):
        return self

    @logofunc(aliases=['fd'])
    def forward(self, v):
        eprint("Forward %i called." % v)
        self.left_motor.run_to_rel_pos(speed_sp=self.speed,
          position_sp = v*self.moving_speed,
          stop_action="hold")
        self.right_motor.run_to_rel_pos(speed_sp=self.speed,
          position_sp = v*self.moving_speed,
          stop_action="hold")
        ## Block the code until the movement is finished
        eprint("  Forward %i waiting to finish." % v)
        self.left_motor.wait_until_not_moving()
        eprint("  Forward %i done." % v)
        # add_command(self.pen.forward, v)
        # add_command(get_canvas().update)

    @logofunc(aliases=['calibrateangle'])
    def calibrate_angle(self):
        eprint("Calibrating angle based on beacon." % v)
        ir = ev3.InfraredSensor()
        while True:
            print(ir.value(0), ir.value(1))
            if ir.value(1) == -128:
              print("Beacon lost, waiting")
              time.sleep(1)
            else:
              # Rotating to face the beacon
              dir = sign(ir.value(0))
        self.left_motor.run_to_rel_pos(speed_sp=self.speed,
          position_sp = v*self.moving_speed,
          stop_action="hold")
        self.right_motor.run_to_rel_pos(speed_sp=self.speed,
          position_sp = v*self.moving_speed,
          stop_action="hold")
        # add_command(self.pen.forward, v)
        # add_command(get_canvas().update)

    @logofunc(aliases=['back', 'bk'])
    def backward(self, v):
        eprint("Backward %i called." % v)
        self.forward(-v)
        # add_command(self.pen.backward, v).add_command(get_canvas().update)

    @logofunc(aliases=['lt'])
    def left(self, v):
        delta = v*self.angle_speed
        lpos = self.left_motor.position
        rpos = self.right_motor.position
        eprint("Left %i called, going for %i from %i L, %i R." % (v, delta, lpos, rpos))
        self.left_motor.run_to_rel_pos(speed_sp=self.speed,
          position_sp = (-1.0)*delta,
          stop_action="hold")
        self.right_motor.run_to_rel_pos(speed_sp=self.speed,
          position_sp = delta,
          stop_action="hold")
        ## Block the code until the movement is finished
        self.left_motor.wait_until_not_moving()
        lpos = self.left_motor.position
        rpos = self.right_motor.position
        eprint("  Left %i done, going for %i to %i L, %i R." % (v, delta, lpos, rpos))
        # add_command(self.pen.left, v)

    @logofunc(aliases=['rt'])
    def right(self, v):
        eprint("Right %i called." % v)
        self.left(-v)
        # add_command(self.pen.right, v)

    @logofunc(aliases=['pu'])
    def penup(self):
        eprint("Pen up called.")
        PenSelector.static_set(NO_PEN)
        # add_command(self.pen.up)

    @logofunc(aliases=['pd'])
    def pendown(self):
        eprint("Pen down called.")
        PenSelector.static_set(self.pen_color)
        # add_command(self.pen.down)

    @logofunc(aware=True)
    def penwidth(self, v):
        eprint("Pen width %i called." % v)
        # add_command(self.pen.width, v)

    @logofunc(aliases=['pc', 'color'],
              arity=1)
    def pencolor(self, *args):
        eprint("Pen color called: ", *args)
        # add_command(self.pen.color, *args)

    @logofunc(aliases=['ht'])
    def hideturtle(self):
        eprint("NOOP: Hide turtle.")
        # add_command(self.pen.tracer, 0)

    @logofunc(aliases=['st'])
    def showturtle(self):
        eprint("NOOP: Show turtle.")
        # add_command(self.pen.tracer, 1)

    @logofunc(aliases=['turtleprint', 'turtlepr'], arity=1)
    def turtlewrite(self, text, move=False):
        if isinstance(text, list):
            text = ' '.join(map(str, text))
        else:
            text = str(text)
        eprint("Turtleprint called: ", text)
        # add_command(self.pen.write, text, move)
        # add_command(get_canvas().update)

    @logofunc()
    def startfill(self):
        eprint("NOOP: Start fill.")
        # add_command(self.pen.fill, 1)

    @logofunc()
    def endfill(self):
        eprint("NOOP: Stop fill.")
        # add_command(self.pen.fill, 0)
        # add_command(get_canvas().update)

    @logofunc()
    def setxy(self, x, y):
        eprint("Goto %i, %i called." % [x, y])
        # add_command(self.pen.goto, x, y)
        # add_command(get_canvas().update)

    @logofunc()
    def setx(self, x):
        eprint("Setx %i called." % x)
        # t = self.pen
        # add_command(t.goto, x, t.position()[1])
        # add_command(get_canvas().update)

    @logofunc()
    def sety(self, y):
        eprint("Sety %i called." % y)
        # t = self.pen
        # add_command(t.goto, t.position()[0], y)
        # add_command(get_canvas().update)

    @logofunc()
    def posx(self):
        return self.pen.position()[0]

    @logofunc()
    def posy(self):
        return self.pen.position()[1]

    @logofunc()
    def heading(self):
        return self.pen.heading()

    @logofunc()
    def setheading(self, v):
        eprint("Setheading %i called." % v)
        # add_command(self.pen.setheading, v)

    @logofunc()
    def home(self):
        eprint("Home %i called.")
        # add_command(self.pen.setheading, 0)
        # add_command(self.pen.goto, 0, 0)
        # add_command(get_canvas().update)

    @logofunc(aliases=['cs', 'clearscreen'])
    def clear(self):
        eprint("NOOP: Clearscreen.")
        # self.home()
        # add_command(self.pen.clear)
        # add_command(get_canvas().update)

    @logofunc(arity=1)
    def distance(self, other, orig=None):
        if orig is None:
            orig = self.pen
        return math.sqrt((orig.position()[0]-other.position()[0])**2 +
                         (orig.position()[1]-other.position()[1])**2)

    @logofunc(aware=True)
    def clone(self, interp):
        new = self.__class__()

@logofunc()
def allturtles():
    return [t() for t in Turtle._all_turtles if t()]

@logofunc(aware=True)
def createturtle(interp, use_turtle = turtle):
    t = Turtle(use_turtle)
    interp.push_actor(t)

def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x
