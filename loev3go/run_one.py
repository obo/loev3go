#!/usr/bin/python3
# Run one hardcoded LOGO program using logo_turtle and saving the canvas
# afterwards.

from pylogo import common
from pylogo import Logo
from pylogo import interpreter
from pylogo import reader
from pylogo import builtins
from pylogo import oobuiltins

import turtle

from pylogo import ps_turtle
interpreter.Logo.import_module(ps_turtle)
ps_turtle.createturtle(interpreter.Logo)

# from pylogo import ev3_turtle
# interpreter.Logo.import_module(ev3_turtle)
# ev3_turtle.createturtle(interpreter.Logo)

code = "fd 10"
code = "for [l 10 80 5] [repeat 5 [repeat 8 [fd :l rt 45] rt 72]"
code = "repeat 10 [fd 40 fd 40 bk 80 rt 1]"
code = """to square
  repeat 4 [ fd 10 rt 90 ]
end
square
"""
code = """to gen :lo :hi :step
  make "x []
  while [ :lo < (:hi+1) ] [ make "x lput :lo :x make "lo :lo + :step ]
  output :x
end
for "l (gen 10 80 5) [print :l]
"""

code = "repeat 8 [repeat 4 [rt 90 fd 100] bk 100 lt 45]"

# interp = interpreter.RootFrame()
interp = Logo
interp.import_module(builtins)
interp.import_module(oobuiltins)
from pylogo import builtins

from io import StringIO
input = StringIO(code)
input.name = '<string>'
tokenizer = reader.FileTokenizer(reader.TrackingStream(input))
interp.push_tokenizer(tokenizer)
try:
    v = interp.expr_top()
    if v is not None:
        print(builtins.logo_repr(v))
finally:
    interp.pop_tokenizer()

turtle.update()
cv = turtle.getcanvas()
cv.postscript(file="file_name.ps", colormode='color')
print("Closing.")
cv.destroy()
print("Destroyed.")

# comm = LogoCommunicator(TheApp, interpreter.Logo)
#self.logo_communicator.add_input(code)

