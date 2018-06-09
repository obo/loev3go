#!/usr/bin/env python3
# Logo interpreter that runs EV3 turtle robot
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

#import turtle
#import tkinter as tk
#import src.canvasvg as canvasvg

from pylogo import ev3_turtle

class LogoOntoCarpet(object):
  def __init__(self, stop_switch):
    interpreter.Logo.import_module(ev3_turtle)

    self.interp = Logo
    self.interp.import_module(builtins)
    self.interp.import_module(oobuiltins)
    self.stop_switch = stop_switch

  def run_logo_robot(self, code):
    input = StringIO(code)
    input.name = '<string>'
    tokenizer = reader.FileTokenizer(reader.TrackingStream(input))
    self.interp.push_tokenizer(tokenizer)
    try:
        while True:
            if self.stop_switch.is_set():
                break;
            tok = self.interp.tokenizer.peek()
            if tok is EOF:
                break
            val = self.interp.expr_top()
    finally:
        self.interp.pop_tokenizer()
