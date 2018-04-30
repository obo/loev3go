#!/usr/bin/python3
# from https://raw.githubusercontent.com/Klabbedi/ev3/master/Line_follow_2.py
# coding: utf-8

from time import sleep

from ev3dev.auto import *

# ------Input--------
print('Setting input values')
power = 60
power = 20
power = 40
target = 55
kp = float(0.65) # Proportional gain. Start value 1
kp = float(0.95) # Proportional gain. Start value 1
kd = 1           # Derivative gain. Start value 0
ki = float(0.02) # Integral gain. Start value 0
direction = -1
  # set to -1 for dark on the right hand side
# identify the min and max with report-color-values.py
minRef = 250 # sub of RGB for the dark *right* side of the line
maxRef = 550 # sub of RGB for the light *left* side of the line
# -------------------

# Connect two large motors on output ports B and C and check that
# the device is connected using the 'connected' property.
print('Connecting motors')
left_motor = LargeMotor(OUTPUT_B);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C); assert right_motor.connected
# One left and one right motor should be connected

# Connect color and touch sensors and check that they
# are connected.
print('Connecting sensors')
#ir = InfraredSensor();         assert ir.connected
ts = TouchSensor();            assert ts.connected
col= ColorSensor();     assert col.connected

# Change color sensor mode
print('Setting color sensor mode')
#col.mode = 'COL-REFLECT'
col.mode = 'RGB-RAW' # use rgb sum

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
                        motor.duty_cycle_sp = pow
                sleep(0.01) # Aprox 100Hz

run(power, target, kp, kd, ki, direction, minRef, maxRef)

# Stop the motors before exiting.
print('Stopping motors')
left_motor.stop()
right_motor.stop()
