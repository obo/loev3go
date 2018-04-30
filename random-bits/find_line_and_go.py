#!/usr/bin/python3
# based on
#   https://raw.githubusercontent.com/Klabbedi/ev3/master/max_min_finder.py
# Place robot approximately on the line, so that rotating left and right would
# show it both sides of the line.
# When the line is found, the robot will follow it.
# coding: utf-8

from time   import time, sleep
from ev3dev.auto import *
from time import sleep

debug = False

# Connect color and touch sensors and check that they
# are connected.
print('Connecting sensors')
ts = TouchSensor();            assert ts.connected
col= ColorSensor();     assert col.connected



# Connect two large motors on output ports B and C and check that
# the device is connected using the 'connected' property.
#print('Connecting motors')
left_motor = LargeMotor(OUTPUT_B);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C); assert right_motor.connected
polarity = -1
  # polarity means where the 'head' of the robot is wrt to motor direction

# Change color sensor mode
print('Setting color sensor mode')
#col.mode = 'COL-REFLECT'
col.mode = 'RGB-RAW' # use rgb sum

print ("Rotating to left and right to find the line.")

speed = 30 # speed of each of the motors

same_color_delta = 100 # all color diffs within this range treated as the same color
distinct_color_delta = 300
# when comparing two colors, they have to differ at least by this

def get_color():
  # sum of RGB
  return col.value(0) + col.value(1) + col.value(2)

def find_stable_color_on_one_side(direction, speed, distinct_from, same_color_time_span, max_time=1.0):
  left_motor.run_direct(duty_cycle_sp=polarity*direction*speed)
  right_motor.run_direct(duty_cycle_sp=polarity*direction*(-1)*speed)
  last = get_color()
  start_time = time.time()
  end_time = start_time + max_time
  col_start_time = start_time
  found_color = -1
  now = time.time()
  while now < end_time:
    curr = get_color()
    if debug:
      print("Curr: "+str(curr)+", Last: "+str(last)+", Found: "+str(found_color))
    if distinct_from == -1 or abs(curr-distinct_from) > distinct_color_delta:
      # only store the current color if distinct from the given color
      if abs(curr - last) > same_color_delta:
        last = curr
        col_start_time = now
      if now - col_start_time > same_color_time_span:
        found_color = last
        break
    now = time.time()
  left_motor.stop()
  right_motor.stop()
  # return back
  back_time = time.time()-start_time
  end_time = time.time() + back_time
  left_motor.run_direct(duty_cycle_sp=polarity*(-1)*direction*speed)
  right_motor.run_direct(duty_cycle_sp=polarity*(-1)*direction*(-1)*speed)
  while time.time() <  end_time:
    pass
  left_motor.stop()
  right_motor.stop()
  print("Found: "+str(found_color))
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

print("Left: "+str(left_color)+", Right: "+str(right_color)+", slower? "+str(slower))

if left_color == -1 or right_color == -1:
  print("Failed to find the line, stopping.")
  exit()

if left_color < right_color:
  direction = -1
  minRef = left_color
  maxRef = right_color
else:
  direction = 1
  minRef = right_color
  maxRef = left_color
# direction = -1
  # set to -1 for dark on the right hand side
# identify the min and max with report-color-values.py
# minRef = 250 # sub of RGB for the dark *right* side of the line
# maxRef = 550 # sub of RGB for the light *left* side of the line


# ------Input--------
#power = 60
#target = 55
power = 20
power = 40
target = int(0.9*power)
kp = float(0.65) # Proportional gain. Start value 1
kp = float(1.95) # Proportional gain. Start value 1
kd = 1           # Derivative gain. Start value 0
ki = float(0.02) # Integral gain. Start value 0
# -------------------


# Adding button so it would be possible to break the loop using
# one of the buttons on the brick
print('Adding button')
btn = Button()

def steering2(course, power):
        """
        Computes how fast each motor in a pair should turn to achieve the
        specified steering.
        Input:
                course [-100, 100]:
                * -100 means turn left as fast as possible,
                *  0   means drive in a straight line, and
                *  100  means turn right as fast as possible.
                * If >100 power_right = -power
                * If <100 power_left = power        
        power: the power that should be applied to the outmost motor (the one
                rotating faster). The power of the other motor will be computed
                automatically.
        Output:
                a tuple of power values for a pair of motors.
        Example:
                for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
                        motor.run_forever(speed_sp=power)
        """
        if course >= 0:
                if course > 100:
                        power_right = 0
                        power_left = power
                else:   
                        power_left = power
                        power_right = power - ((power * course) / 100)
        else:
                if course < -100:
                        power_left = 0
                        power_right = power
                else:
                        power_right = power
                        power_left = power + ((power * course) / 100)
        return (int(power_left), int(power_right))

def steering3(course, power):
        """
        Computes how fast each motor in a pair should turn to achieve the
        specified steering.
        Compared to steering2, this alows pivoting.
        Input:
                course [-100, 100]:
                * -100 means turn left as fast as possible (running left
                * backwards)
                * -50  means quick turn, left stopped
                *  0   means drive in a straight line, and
                *  50  means quick turn, right stopped
                *  100  means turn right as fast as possible (right backwards)
                * If >100 power_right = -power
                * If <100 power_left = power        
        power: the power that should be applied to the outmost motor (the one
                rotating faster). The power of the other motor will be computed
                automatically.
        Output:
                a tuple of power values for a pair of motors.
        Example:
                for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
                        motor.run_forever(speed_sp=power)
        """
        abscourse = min(abs(course), 100)
        outer = power
        inner = (abscourse - 50)/50*power
        if course >= 0:
          power_left = outer
          power_right = inner
        else:
          power_right = outer
          power_left = inner
        return (int(power_left), int(power_right))

def run(power, target, kp, kd, ki, direction, minRef, maxRef):
        """
        PID controlled line follower algoritm used to calculate left and right motor power.
        Input:
                power. Max motor power on any of the motors
                target. Normalized target value.
                kp. Proportional gain
                ki. Integral gain
                kd. Derivative gain
                direction. 1 or -1 depending on the direction the robot should steer
                minRef. Min reflecting value of floor or line
                maxRef. Max reflecting value of floor or line 
        """
        lastError = error = integral = 0
        left_motor.run_direct()
        right_motor.run_direct()
        while not btn.any() :
                if ts.value():
                       print('Breaking loop')# User pressed touch sensor
                       break
                #refRead = col.value()
                refRead = col.value(0)+col.value(1)+col.value(2)
                error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
                derivative = error - lastError
                lastError = error
                integral = float(0.5) * integral + error
                course = (kp * error + kd * derivative +ki * integral) * direction
                for (motor, pow) in zip((left_motor, right_motor), steering3(course, power)):
                        motor.duty_cycle_sp = polarity*pow
                sleep(0.01) # Aprox 100Hz

run(power, target, kp, kd, ki, direction, minRef, maxRef)

# Stop the motors before exiting.
print('Stopping motors')
left_motor.stop()
right_motor.stop()

