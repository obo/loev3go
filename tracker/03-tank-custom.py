#!/usr/bin/env python3


import logging
import threading
import signal
import time
import ev3dev.ev3 as ev3
import sys
from ev3dev.auto import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev.helper import MediumMotor

logging.basicConfig(level=logging.DEBUG,
          format='%(asctime)s %(levelname)5s: %(message)s')
log = logging.getLogger(__name__)

log.info("Starting TRACK3RWithClaw")



class Tank(object):
  def __init__(self, left_motor, right_motor, polarity='normal', name='Tank',
               speed_sp=400):
    self.left_motor = ev3.LargeMotor(left_motor)
    self.right_motor = ev3.LargeMotor(right_motor)

    for x in (self.left_motor, self.right_motor):
      if not x.connected:
        log.error("%s is not connected" % x)
        sys.exit(1)

    self.left_motor.reset()
    self.right_motor.reset()
    self.speed_sp = speed_sp
    self.left_motor.speed_sp = self.speed_sp
    self.right_motor.speed_sp = self.speed_sp
    self.set_polarity(polarity)
    self.name = name
    log.info("Created Tank object "+name+" for speed "+str(self.speed_sp))

  def __str__(self):
    return self.name

  def set_polarity(self, polarity):
    valid_choices = ('normal', 'inversed')
    assert polarity in valid_choices,\
      "%s is an invalid polarity choice, must be %s" % (polarity, ', '.join(valid_choices))

    self.left_motor.polarity = polarity
    self.right_motor.polarity = polarity


class RemoteControlledTank(Tank):

  def __init__(self, left_motor, right_motor, polarity='normal', channel=1, speed_sp=400):
    Tank.__init__(self, left_motor, right_motor, polarity, speed_sp=speed_sp)
    log.info("Getting remote control for channel "+str(channel))
    self.remote = ev3.RemoteControl(channel=channel)

    if not self.remote.connected:
      log.error("%s is not connected" % self.remote)
      sys.exit(1)

    self.remote.on_red_up = self.make_move(self.left_motor, self.speed_sp)
    self.remote.on_red_down = self.make_move(self.left_motor, self.speed_sp * -1)
    self.remote.on_blue_up = self.make_move(self.right_motor, self.speed_sp)
    self.remote.on_blue_down = self.make_move(self.right_motor, self.speed_sp * -1)

  def make_move(self, motor, dc_sp):
    def move(state):
      if state:
        motor.run_forever(speed_sp=dc_sp)
      else:
        motor.stop()
    return move

  def main(self, done):

    try:
      while not done.is_set():
        self.remote.process()
        time.sleep(0.01)

    # Exit cleanly so that all motors are stopped
    except (KeyboardInterrupt, Exception) as e:
      log.exception(e)

      for motor in ev3.list_motors():
        motor.stop()


class TRACK3R(RemoteControlledTank):
    """
    Base class for all TRACK3R variations. The only difference in the child
    classes are in how the medium motor is handled.

    To enable the medium motor toggle the beacon button on the EV3 remote.
    """

    def __init__(self, medium_motor, left_motor, right_motor, speed_sp=400, channel=1):
        RemoteControlledTank.__init__(self, left_motor, right_motor, speed_sp=speed_sp, channel=channel)
        self.medium_motor = MediumMotor(medium_motor)

        if not self.medium_motor.connected:
            log.error("%s is not connected" % self.medium_motor)
            sys.exit(1)

        self.medium_motor.reset()



class TRACK3RWithClaw(TRACK3R):

    def __init__(self, medium_motor=OUTPUT_A, left_motor=OUTPUT_B, right_motor=OUTPUT_C, speed_sp=400, channel=1):
        TRACK3R.__init__(self, medium_motor, left_motor, right_motor, speed_sp=speed_sp, channel=channel)
        self.remote.on_beacon = self.move_claw

    def move_claw(self, state):
        if state:
            self.medium_motor.run_to_rel_pos(speed_sp=200, position_sp=-75)
        else:
            self.medium_motor.run_to_rel_pos(speed_sp=200, position_sp=75)



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
    time.sleep(0.5)

# The 'done' event will be used to signal the threads to stop:
done = threading.Event()

# We also need to catch SIGINT (keyboard interrup) and SIGTERM (termination
# signal from brickman) and exit gracefully:
def signal_handler(signal, frame):
  done.set()

signal.signal(signal.SIGINT,  signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


trackerBasic = TRACK3RWithClaw()
trackerFast = TRACK3RWithClaw(channel=2, speed_sp=800)
#trackerSlow = TRACK3RWithClaw(channel=3, speed_sp=200)

# Now that we have the worker functions defined, lets run those in separate
# threads.
#touchthread = threading.Thread(target=touch_leds,    args=(done,))
colorthread = threading.Thread(target=color_speaker, args=(done,))
fastthread = threading.Thread(target=trackerFast.main, args=(done,))

#touchthread.start()
colorthread.start()
fastthread.start()

log.info("Started TRACK3RWithClaw")
ev3.Sound.speak("I'm ready!")

trackerBasic.main(done)
# hopefully it will be sufficient to start one
ev3.Sound.speak("Exiting!")
log.info("Exiting TRACK3RWithClaw")

done.set()
#touchthread.join()
colorthread.join()
fastthread.join()
