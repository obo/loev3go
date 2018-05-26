# Postscript turtle, direct drawing on plain canvas from python turtle graphics
# Exporting the canvas then to postscript

# dbg print
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


import turtle
import math
import weakref
import threading
import sys

from pylogo.common import *

update = False
  # update after ever step

get_canvas = turtle.getcanvas

class Turtle:

    _all_turtles = []
    _turtle_count = 1

    def __init__(self):
        self.pen = turtle # use plain turtle graphics
        self.pen.degrees()
        turtle.tracer(False)
        turtle.ht()
        self.pen.speed(0)
        # I don't know why more turtles should be supported:
        self._all_turtles.append(weakref.ref(self))
        self._count = self._turtle_count
        self.__class__._turtle_count += 1

    def __repr__(self):
        return '<%s %i>' % (self.__class__.__name__,
                            self._count)

    @logofunc()
    def turtle(self):
        return self

    @logofunc(aliases=['fd'])
    def forward(self, v):
        self.pen.forward(v)
        if update: get_canvas().update()

    @logofunc(aliases=['back', 'bk'])
    def backward(self, v):
        self.pen.backward(v)
        if update: get_canvas().update()

    @logofunc(aliases=['lt'])
    def left(self, v):
        self.pen.left(v)

    @logofunc(aliases=['rt'])
    def right(self, v):
        self.pen.right(v)

    @logofunc(aliases=['pu'])
    def penup(self):
        self.pen.up()

    @logofunc(aliases=['pd'])
    def pendown(self):
        self.pen.down()

    @logofunc(aware=True)
    def penwidth(self, v):
        self.pen.width(v)

    @logofunc(aliases=['pc', 'color'],
              arity=1)
    def pencolor(self, *args):
        self.pen.color(*args)

    @logofunc(aliases=['ht'])
    def hideturtle(self):
        self.pen.tracer(0)

    @logofunc(aliases=['st'])
    def showturtle(self):
        self.pen.tracer(1)

    @logofunc(aliases=['turtleprint', 'turtlepr'], arity=1)
    def turtlewrite(self, text, move=False):
        if isinstance(text, list):
            text = ' '.join(map(str, text))
        else:
            text = str(text)
        self.pen.write(text, move)
        if update: get_canvas().update()

    @logofunc()
    def startfill(self):
        self.pen.fill(1)

    @logofunc()
    def endfill(self):
        self.pen.fill(0)
        if update: get_canvas().update()

    @logofunc()
    def setxy(self, x, y):
        self.pen.goto(x, y)
        if update: get_canvas().update()

    @logofunc()
    def setx(self, x):
        t = self.pen
        t.goto(x, t.position()[1])
        if update: get_canvas().update()

    @logofunc()
    def sety(self, y):
        t = self.pen
        t.goto(t.position()[0], y)
        if update: get_canvas().update()

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
        self.pen.setheading(v)

    @logofunc()
    def home(self):
        self.pen.setheading(0)
        self.pen.goto(0, 0)
        if update: get_canvas().update()

    @logofunc(aliases=['cs', 'clearscreen'])
    def clear(self):
        self.home()
        self.pen.clear()
        if update: get_canvas().update()

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
def createturtle(interp):
    t = Turtle()
    interp.push_actor(t)
