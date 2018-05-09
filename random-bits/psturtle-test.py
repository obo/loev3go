#!/usr/bin/python
# runme as: xvfb-run psturtle-test.py
import turtle

turtle.speed(0) # no animation
turtle.ht() # no turtle visible
turtle.color('red', 'yellow')
turtle.begin_fill()
while True:
    turtle.forward(200)
    turtle.left(170)
    if abs(turtle.pos()) < 1:
        break
turtle.end_fill()
turtle.update()
cv = turtle.getcanvas()
cv.postscript(file="file_name.ps", colormode='color')
print("Closing.")
cv.destroy()
print("Destroyed.")
