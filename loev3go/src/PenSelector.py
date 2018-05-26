#!/usr/bin/env python3
# Handle the 2 pens controlled by medium motor
# Assumes that the medium motor is in port OUTPUT_A
# Assumes that the program has started with no pen down
# Assumes that his module is imported only at the beginning of the program
#   (because it resets the motor state)

import ev3dev.ev3 as ev3
from ev3dev.auto import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev.helper import MediumMotor

LEFT_PEN = 'penL'
RIGHT_PEN = 'penR'
NO_PEN = 'penUP'

pen_position = { LEFT_PEN:-30, NO_PEN:0, RIGHT_PEN:+30 }
pen_shift_speed = 80
med_motor = ev3.MediumMotor(medium_motor_output)
med_motor.reset() # set motor position to 0
# assuming we start with both pens up
pen_state = NO_PEN

pen_cycle = [LEFT_PEN, NO_PEN, RIGHT_PEN, NO_PEN]
pen_cycle_state = len(pen_shifts)-1 # the last pen state

class PenSelector(object):
  """To access the pen, create a pen selector object.
  The object can be created many times or just once.
  The object serves only as a wrapper that hides global variable on pen state
  """

  def __init__(self):
    pass

  def set(self, newstate):
    """Set a particular pen state"""
    static_set(newstate)
    
  @staticmethod
  def static_set(newstate):
    global med_motor
    global pen_state
    med_motor.run_to_abs_pos(
      speed_sp = pen_shift_speed,
      position_sp = pen_position[newstate],
      stop_action = "hold")
    pen_state = newstate
    
  def next(self):
    """Move to the next pen state from the pre-defined cycle"""
    static_next()

  @staticmethod
  def static_next():
    global pen_cycle_state
    pen_cycle_state = (pen_cycle_state+1) % len(pen_cycle)
    self.set(pen_cycle[pen_cycle_state])

