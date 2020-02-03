#!/usr/bin/env python3
# Manually-controlled turtle with two pens
# Functionality:
#  IR channel 0: normal
#  IR channel 1: fast
#  IR channel 2: slow
#  Beacon button (all 3 channels): toggle pens
# Synopsis:
#  ... see __main__ below


import math
import logging
import threading
import time
import ev3dev.ev3 as ev3
import sys
from ev3dev.auto import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

import PenSelector

logging.basicConfig(level=logging.DEBUG,
          format='%(asctime)s %(levelname)5s: %(message)s')
log = logging.getLogger(__name__)

log.info("Starting TRACK3RWithPen")

silent = True

#### Helper functions

def play_leds():
  """Indicate that we've started"""
  from ev3dev.ev3 import Leds
  # save current state
  saved_state = [led.brightness_pct for led in Leds.LEFT + Leds.RIGHT]
  Leds.all_off()
  time.sleep(0.1)
  for _ in range(1):
    for color in (Leds.RED, Leds.YELLOW, Leds.GREEN):
        for group in (Leds.LEFT, Leds.RIGHT):
            Leds.set_color(group, color)
        time.sleep(0.1)
  Leds.all_off()
  time.sleep(0.5)
  for led, level in zip(Leds.RIGHT + Leds.LEFT, saved_state) :
      led.brightness_pct = level

#### Main classes


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
      self.remote = None # won't respond to remote
    else:
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
    if self.remote:
      self.remote.process()

  def main(self, done):
    if self.remote:
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
    """

    def __init__(self, left_motor, right_motor, speed_sp=400, channel=1):
        RemoteControlledTank.__init__(self, left_motor, right_motor, speed_sp=speed_sp, channel=channel)



class TRACK3RWithPen(TRACK3R):
    """
    Deviating from ev3dev-lang-python demo TRACK3R, we use beacon to toggle the
    pens
    """

    def __init__(self, pen_selector, left_motor=OUTPUT_B, right_motor=OUTPUT_C, speed_sp=400, channel=1):
        TRACK3R.__init__(self, left_motor, right_motor, speed_sp=speed_sp, channel=channel)
        if self.remote:
          self.remote.on_change = self.handle_changed_buttons
        self.pen_selector = pen_selector
        # self.remote.on_beacon = self.toggle_pen
        # we can't use the on_beacon because beacon gets dropped whenever we move

    def handle_changed_buttons(self, changed_buttons):
      # The goal is to run toggle_pen only when beacon event happens *alone*
      # print("Changed buttons: ", changed_buttons)
      if len(changed_buttons) == 1 and changed_buttons[0][0] == 'beacon':
        self.toggle_pen()


    def toggle_pen(self):
        self.pen_selector.next()

class SpeedableTrackerWithPen:
    """A combination of three trackers of various speeds"""
    def __init__(self, done, medmotor=OUTPUT_A):
      # The 'done' event will be used to signal the threads to stop:
      #   done = threading.Event()
      self.done = done
      self.pen_selector=PenSelector.PenSelector()
      self.trackers = [
        TRACK3RWithPen(self.pen_selector, channel=1, speed_sp=400),
        TRACK3RWithPen(self.pen_selector, channel=2, speed_sp=800),
        TRACK3RWithPen(self.pen_selector, channel=3, speed_sp=200)
      ]
      play_leds()

    def __del__(self):
      for motor in ev3.list_motors():
        motor.stop(stop_action='coast')

    def run(self):
      while not self.done.is_set():
        for tracker in self.trackers:
          tracker.process()
        time.sleep(0.01)

    """
    Unsure if we need to catch exceptions here, hopefully the destructor will
    be sufficient
    def run(self):
      try:
        while not self.done.is_set():
          for tracker in self.trackers:
            tracker.process()
          time.sleep(0.01)
      # Exit cleanly so that all motors are stopped
      except (KeyboardInterrupt, Exception) as e:
        self.done.set()
        for motor in ev3.list_motors():
          motor.stop(stop_action='coast')
    """


if __name__ == "__main__":
  """When run as script, run the tracker"""
  import threading, signal
  done = threading.Event() # set this to stop gracefully
  def signal_handler(signal, frame):
    done.set()
  signal.signal(signal.SIGINT,  signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)
  t = SpeedableTrackerWithPen(done)
  t.run() # or launch this in a thread, it will finish after done has been set


