import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor()
cl.mode='RGB-RAW'
print("Calibrating, hopefully looking at something white now.")
cl.calibrate_white()
while True:
    red = cl.value(0)
    green=cl.value(1)
    blue=cl.value(2)
    print("Red: " + str(red) + ", Green: " + str(green) + ", Blue: " + str(blue))
    time.sleep(1)
