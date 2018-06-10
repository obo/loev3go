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

from pylogo import ev3_turtle

class LogoOntoCarpet(object):
  def __init__(self, should_stop, stopped):
    # should_stop is something that we check and stop
    # stopped is something that we set just before finishing
    interpreter.Logo.import_module(ev3_turtle)

    # create our custom global-level interpreter object
    self.interp = interpreter.RootFrame()
    self.interp.import_module(builtins)
    self.interp.import_module(oobuiltins)
    self.should_stop = should_stop
    self.stopped = stopped
    self.stopped.set() # when we start, the robot is not running

  def run_logo_robot(self, code):
    self.stopped.clear()
      # indicate that we are running
    # create our logo-runner turtle with the python turtle
    ev3_turtle.createturtle(self.interp, self.should_stop)
    input = StringIO(code)
    input.name = '<string>'
    tokenizer = reader.FileTokenizer(reader.TrackingStream(input))
    self.interp.push_tokenizer(tokenizer)
    try:
        while True:
            if self.should_stop.is_set():
                break;
            tok = self.interp.tokenizer.peek()
            if tok is EOF:
                break
            val = self.interp.expr_top()
    except ev3_turtle.UserStoppedRobot as reason:
      pass
    except common.LogoError as e:
      pass
    finally:
        self.interp.pop_tokenizer()
        self.stopped.set()
