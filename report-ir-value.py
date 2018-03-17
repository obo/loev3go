import ev3dev.ev3 as ev3
import time

ir = ev3.InfraredSensor()
while True:
    print(ir.value(0), ir.value(1))
    #print(ir0.value(), ir1.value())
    time.sleep(1)
