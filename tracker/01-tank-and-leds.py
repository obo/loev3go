#!/usr/bin/env python3

import logging
from TRACK3R import TRACK3RWithClaw
import threading
import signal
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
head = threading.Thread(target=touch_leds,   args=(done,))

head.start()

log.info("Started TRACK3RWithClaw")
ev3.Sound.speak("I'm ready!")

tracker = TRACK3RWithClaw()
tracker.main()
log.info("Exiting TRACK3RWithClaw")

done.set()
head.join()
