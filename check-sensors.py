#!/usr/bin/env python3
# Test the hardware config needed by loev3go

import ev3dev.ev3 as ev3
from ev3dev.auto import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

# assumed connections
medium_motor_output = OUTPUT_A
left_motor=OUTPUT_B
right_motor=OUTPUT_C
channel=1

# test if remote is connected
remote = ev3.RemoteControl(channel=channel)

# test motors
left_motor = ev3.LargeMotor(left_motor)
right_motor = ev3.LargeMotor(right_motor)
med_motor = ev3.MediumMotor(medium_motor_output)

for m in [left_motor, right_motor, med_motor]:
  assert m.connected
  m.run_to_rel_pos(speed_sp=150, position_sp = 10, stop_action="stop")
  m.run_to_rel_pos(speed_sp=150, position_sp = -10, stop_action="stop")


