#!/usr/bin/env python3
# Logo interpreter that creates SVG images
# Synopsis:
#  ... see __main__ below

from pylogo import common
from pylogo import Logo
from pylogo import interpreter
from pylogo import reader
from pylogo import builtins
from pylogo import oobuiltins

from pylogo.common import EOF
from pylogo import builtins

from io import StringIO

import turtle
import tkinter as tk
import src.canvasvg as canvasvg

from pylogo import ps_turtle

class LogoIntoSVG(object):
  def __init__(self):
    interpreter.Logo.import_module(ps_turtle)

    self.interp = Logo
    self.interp.import_module(builtins)
    self.interp.import_module(oobuiltins)

  def run_logo_emit_svg(self, code, outfile):
    # create a new canvas
    f = tk.Frame(None).pack()
    cv = tk.Canvas(master=f,width=500,height=500)
    cv.pack()
    # create a python turtle on it
    t = turtle.RawTurtle(cv, shape='square', visible=False)
    # run that turtle superfast
    t._tracer(0, None)
    # create our logo-runner turtle with the python turtle
    ps_turtle.createturtle(self.interp, t)
    # tokenize the given code
    input = StringIO(code)
    input.name = '<string>'
    tokenizer = reader.FileTokenizer(reader.TrackingStream(input))
    self.interp.push_tokenizer(tokenizer)
    try:
        while True:
            tok = self.interp.tokenizer.peek()
            if tok is EOF:
                break
            val = self.interp.expr_top()
    finally:
        self.interp.pop_tokenizer()
    t.screen.update()
    #cv = turtle.getcanvas()
    canvasvg.saveall(outfile, cv)
    print("Closing.")
    cv.destroy()
    print("Destroyed.")
