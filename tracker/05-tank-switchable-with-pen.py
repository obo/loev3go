#!/usr/bin/env python3
# Functionality:
#  IR channel 0: normal tank
#  IR channel 1: fast tank
#  IR channel 2: slow tank
#  backspace -> exit
#  down -> toggle color saying
#  up -> follow the current color


import math
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

log.info("Starting TRACK3RWithPen")

silent = True

class Tank(object):
  def __init__(self, left_motor, right_motor, polarity='inversed', name='Tank',
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

  def __init__(self, left_motor, right_motor, polarity='inversed', channel=1, speed_sp=400):
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

  def process(self):
    self.remote.process()

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


pen_state = 0
pen_positions = [30, 0, 30, 60]
# 30 ... pens up
# 0 ... left pen down
# 60 ... right pen down
m=MediumMotor(OUTPUT_A)
m.run_to_abs_pos(speed_sp=80, position_sp=pen_positions[pen_state], stop_action="hold")
# lift both pens

class TRACK3RWithPen(TRACK3R):

    def __init__(self, medium_motor=OUTPUT_A, left_motor=OUTPUT_B, right_motor=OUTPUT_C, speed_sp=400, channel=1):
        TRACK3R.__init__(self, medium_motor, left_motor, right_motor, speed_sp=speed_sp, channel=channel)
        self.remote.on_change = self.handle_changed_buttons
        # self.remote.on_beacon = self.toggle_pen
        # we can't use the on_beacon because beacon gets dropped whenever we move

    def handle_changed_buttons(self, changed_buttons):
      # The goal is to run toggle_pen only when beacon event happens *alone*
      # print("Changed buttons: ", changed_buttons)
      if len(changed_buttons) == 1 and changed_buttons[0][0] == 'beacon':
        self.toggle_pen()


    def toggle_pen(self):
        global pen_state
        pen_state = (pen_state+1) % len(pen_positions)
        print("New pen state:", pen_state)
        self.medium_motor.run_to_abs_pos(speed_sp=80, position_sp=pen_positions[pen_state], stop_action="hold")



def touch_leds(done):
  """
  This is the second thread of execution. It will constantly poll the
  touch button and change leds
  """
  ts = ev3.TouchSensor()
  while not done.is_set():
    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])


def play_leds(self):
  from ev3dev.ev3 import Leds
  # save current state
  saved_state = [led.brightness_pct for led in Leds.LEFT + Leds.RIGHT]
  Leds.all_off()
  time.sleep(0.1)
  # continuous mix of colors
  print('colors fade')
  for i in range(180):
      rd = math.radians(10 * i)
      Leds.red_left.brightness_pct = .5 * (1 + math.cos(rd))
      Leds.green_left.brightness_pct = .5 * (1 + math.sin(rd))
      Leds.red_right.brightness_pct = .5 * (1 + math.sin(rd))
      Leds.green_right.brightness_pct = .5 * (1 + math.cos(rd))
      time.sleep(0.05)
  Leds.all_off()
  time.sleep(0.5)
  for led, level in zip(Leds.RIGHT + Leds.LEFT, saved_state) :
      led.brightness_pct = level


def toggle_event(evt):
  if evt.is_set():
    log.info("toggling off")
    evt.clear()
  else:
    log.info("toggling on")
    evt.set()

def button_watcher(done):
  """
  This will respond to buttons pressed
  """
  bt = ev3.Button()
  log.info("Configuring buttons:")
  # the horrifying lambda-if-not-x-else-true runs play_leds upon button release
  bt.on_up = lambda x: play_leds if not x else True
  log.info("  up:  play_leds")
  bt.on_backspace = lambda x: done.set() if not x else True
  log.info("  esc:  exit")

  bt.on_down = lambda x: toggle_event(color_speaker_on) if not x else True
    # toggle operation of color speaker
  log.info("  down:  speak colors")
  while not done.is_set():
    bt.process()
    time.sleep(0.5)


def color_speaker(done, color_speaker_on):
  """
  This will poll color and say its name if changed.
  """
  while not done.is_set():
    log.info("color_speaker ready")
    color_speaker_on.wait() # wait until someone launches us
    log.info("color_speaker starting")
    cl = ev3.ColorSensor()
    assert cl.connected, "Connect a color sensor to any sensor port"
    cl.mode='COL-COLOR'
    colors=('unknown','black','blue','green','yellow','red','white','brown')
    lastcolor=0
    while color_speaker_on.is_set() and not done.is_set():
      thiscolor = cl.value()
      if thiscolor != lastcolor:
        lastcolor = thiscolor
        if thiscolor:
          print(colors[thiscolor])
          ev3.Sound.speak("This is "+colors[thiscolor]+".").wait()
      time.sleep(0.5)
    log.info("color_speaker stopping")

# The 'done' event will be used to signal the threads to stop:
done = threading.Event()

# global switches
color_speaker_on = threading.Event()


# We also need to catch SIGINT (keyboard interrup) and SIGTERM (termination
# signal from brickman) and exit gracefully:
def signal_handler(signal, frame):
  done.set()

signal.signal(signal.SIGINT,  signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


trackerBasic = TRACK3RWithPen()
trackerFast = TRACK3RWithPen(channel=2, speed_sp=800)
trackerSlow = TRACK3RWithPen(channel=3, speed_sp=200)

# Now that we have the worker functions defined, lets run those in separate
# threads.
#touchthread = threading.Thread(target=touch_leds,    args=(done,))
colorthread = threading.Thread(target=color_speaker, args=(done, color_speaker_on))
buttonthread = threading.Thread(target=button_watcher, args=(done,))

#touchthread.start()
colorthread.start()
buttonthread.start()

log.info("Started TRACK3RWithPen")
if not silent: ev3.Sound.speak("I'm ready!")

#trackerBasic.main(done)
# our custom loop processing all speeds:
try:
  while not done.is_set():
    trackerBasic.process()
    trackerFast.process()
    trackerSlow.process()
    time.sleep(0.01)
# Exit cleanly so that all motors are stopped
except (KeyboardInterrupt, Exception) as e:
  log.exception(e)
  done.set()
  for motor in ev3.list_motors():
    motor.stop()

# hopefully it will be sufficient to start one
if not silent: ev3.Sound.speak("Exiting!")
log.info("Exiting TRACK3RWithPen")

# release all threads to let them stop
color_speaker_on.set()

done.set()
#touchthread.join()
colorthread.join()
buttonthread.join()
