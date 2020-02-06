#!/usr/bin/python3
# Run two hardcoded LOGO programs using and save the canvas afterwards.
# Run me in xvfb to avoid the need for a running X server:
#   xvfb-run ./test_logo_into_svg.py

import src.LogoIntoSVG

lis=src.LogoIntoSVG.LogoIntoSVG()
lis.run_logo_emit_svg(
"""to square
  repeat 4 [ fd 10 rt 90 ]
end
square
""", "test-square.svg")

lis.run_logo_emit_svg(
"""to gen :lo :hi :step
  make "x []
  while [ :lo < (:hi+1) ] [ make "x lput :lo :x make "lo :lo + :step ]
  output :x
end
for "l (gen 10 30 5) [repeat 5 [repeat 8 [fd :l rt 45] rt 72]]
""", "test-shape.svg")


