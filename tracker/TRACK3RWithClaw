#!/usr/bin/env python3

import logging
from TRACK3R import TRACK3RWithClaw
import threading
import signal
from time   import sleep
import ev3dev.ev3 as ev3

logging.basicConfig(level=logging.DEBUG,
          format='%(asctime)s %(levelname)5s: %(message)s')
log = logging.getLogger(__name__)

log.info("Starting TRACK3RWithClaw")


def touch_leds(done):
  """
  This is the second thread of execution. It will constantly poll the
  touch button and change leds
  """
  ts = ev3.TouchSensor()
  while not done.is_set():
    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])

def color_speaker(done):
  """
  This will poll color and say its name if changed.
  """
  cl = ev3.ColorSensor()
  assert cl.connected, "Connect a color sensor to any sensor port"
  cl.mode='COL-COLOR'
  colors=('unknown','black','blue','green','yellow','red','white','brown')
  lastcolor=0
  while not done.is_set():
    thiscolor = cl.value()
    if thiscolor != lastcolor:
      lastcolor = thiscolor
      if thiscolor:
        print(colors[thiscolor])
        ev3.Sound.speak("This is "+colors[thiscolor]+".").wait()
    sleep(0.5)

# The 'done' event will be used to signal the threads to stop:
done = threading.Event()

# We also need to catch SIGINT (keyboard interrup) and SIGTERM (termination
# signal from brickman) and exit gracefully:
def signal_handler(signal, frame):
  done.set()

signal.signal(signal.SIGINT,  signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Now that we have the worker functions defined, lets run those in separate
# threads.
touchthread = threading.Thread(target=touch_leds,    args=(done,))
colorthread = threading.Thread(target=color_speaker, args=(done,))

touchthread.start()
colorthread.start()

log.info("Started TRACK3RWithClaw")
ev3.Sound.speak("I'm ready!")

tracker = TRACK3RWithClaw()
tracker.main()
ev3.Sound.speak("Exiting!")
log.info("Exiting TRACK3RWithClaw")

done.set()
touchthread.join()
colorthread.join()
