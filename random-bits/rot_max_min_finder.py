#!/usr/bin/python
# based on
#   https://raw.githubusercontent.com/Klabbedi/ev3/master/max_min_finder.py
# Place robot approximately on the line, so that rotating left and right would
# show it both sides
# line.
# coding: utf-8

from time   import time, sleep

from ev3dev.auto import *

print ("Will run for 3 seconds, should cross the line, to report the min and max reflected value")

left_motor = LargeMotor(OUTPUT_B);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C); assert right_motor.connected
col = ColorSensor();         assert col.connected
col.mode = 'RGB-RAW'

speed = 30 # speed of each of the motors

same_color_delta = 100 # all color diffs within this range treated as the same color
distinct_color_delta = 300
# when comparing two colors, they have to differ at least by this

def get_color():
  # sum of RGB
  return col.value(0) + col.value(1) + col.value(2)

def find_stable_color_on_one_side(direction, speed, distinct_from, same_color_time_span, max_time=1.0):
  left_motor.run_direct(duty_cycle_sp=direction*speed)
  right_motor.run_direct(duty_cycle_sp=direction*(-1)*speed)
  last = get_color()
  start_time = time()
  end_time = end_time + max_time
  col_start_time = start_time
  found_color = -1
  now = time()
  while now < end_time:
    curr = get_color()
    print("Curr: "+str(curr)+", Last: "+str(last)+", Found: "+found_color)
    if distinct_from == -1 or abs(curr-distinct_from) > distinct_color_delta:
      # only store the current color if distinct from the given color
      if abs(curr - last) > color_delta:
        last = curr
        col_start_time = now
      if now - col_start_time > same_color_time_span:
        found_color = last
        break
    now = time()
  left_motor.stop()
  right_motor.stop()
  # return back
  back_time = time()-start_time
  end_time = time() + back_time
  left_motor.run_direct(duty_cycle_sp=(-1)*direction*speed)
  right_motor.run_direct(duty_cycle_sp=(-1)*direction*(-1)*speed)
  while time() <  end_time:
    true
  left_motor.stop()
  right_motor.stop()
  return found_color
  # print 'Max: ' + str(max_ref)
  # print 'Min: ' + str(min_ref)


same_color_time_span = 0.2
max_time = 2.0
slower = False # did we need to go slower?

left_color = find_stable_color_on_one_side(+1, speed, -1, same_color_time_span, max_time)
if left_color == --1:
  # try searching slower:
  left_color = find_stable_color_on_one_side(+1, speed/2, -1, same_color_time_span, max_time)
  slower = True
if left_color != -1:
  # now search for the right color
  right_color = find_stable_color_on_one_side(-1, speed, left_color, same_color_time_span, max_time)
  if right_color == -1:
    right_color = find_stable_color_on_one_side(-1, speed/2, left_color, same_color_time_span, max_time)
  slower = True

print("Left: "+left_color+", Right: "+right_color+", slower? "+str(slower))


