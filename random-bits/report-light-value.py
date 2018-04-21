import ev3dev.ev3 as ev3
import time

colors=('unknown','black','blue','green','yellow','red','white','brown')
cl = ev3.ColorSensor()
while True:
    cl.mode='COL-AMBIENT'
    amb = cl.value()
    cl.mode='COL-REFLECT'
    refl = cl.value()
    cl.mode='COL-COLOR'
    col = cl.value()
    print("Ambient: "+str(amb)+", Reflected: "+str(refl)+", Color: "+colors[col] )
    time.sleep(1)
