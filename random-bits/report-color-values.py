import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor()
cl.mode='RGB-RAW'
#print("Calibrating, hopefully looking at something white now.")
#cl.calibrate_white()
## does not seem to be in the released version yet
while True:
    red = cl.value(0)
    green=cl.value(1)
    blue=cl.value(2)
    print("Sum: "+str(red+green+blue)+", Red: " + str(red) + ", Green: " + str(green) + ", Blue: " + str(blue))
    time.sleep(1)
