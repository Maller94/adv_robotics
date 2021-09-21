#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

### Initialization ###
# Create your objects here.
ev3 = EV3Brick()

# Start sound
ev3.speaker.beep(frequency=500, duration=100)

# Initialize the motors.
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.D)

# Initialize the color sensor.
lineRight = ColorSensor(Port.S4)
lineMid = ColorSensor(Port.S2)
lineLeft = ColorSensor(Port.S1)

# Initialize the drive base.
robot = DriveBase(leftMotor, rightMotor, wheel_diameter = 450, axle_track = 100)
speed = 800
turn_angle = 900
adjust_forward = 400
right = 600
left = -600
black = 17


### Planner ###
states_read = ''
with open('plan.txt','r') as r:
    states_read = r.read()
states = states_read.strip("][").split(', ')
states = [x.strip("'") for x in states]

old_state = 'init'
current_state = 'init'

lock_states = True
lock_behavior = True

print(states)

def turn_move(angle):
    robot.straight(adjust_forward)
    robot.turn(angle)
    robot.straight(adjust_forward)


def reverse_move(): 
    robot.straight(-1000)
    robot.turn(1800)

def move_behavior(current_state_inner,old_state_inner):
    # Current state right
    global lock_behavior
    if current_state_inner.lower() == 'r' and old_state_inner.lower() == 'u':
        if lock_behavior == True:
            turn_move(turn_angle)
            lock_behavior = False
    elif current_state_inner.lower() == 'r' and old_state_inner.lower() == 'd':
        if lock_behavior == True:
            turn_move(-turn_angle)
            lock_behavior = False
    elif current_state_inner.lower() == 'r' and old_state_inner.lower() == 'r':
        robot.drive(speed, 0)
    elif current_state_inner.lower() == 'r' and old_state_inner.lower() == 'l':
        if lock_behavior == True:
            reverse_move()
            lock_behavior = False

    # Current state left
    elif current_state_inner.lower() == 'l' and old_state_inner.lower() == 'u':
        if lock_behavior == True:
            turn_move(-turn_angle)
            lock_behavior = False
    elif current_state_inner.lower() == 'l' and old_state_inner.lower() == 'd':
        if lock_behavior == True:
            turn_move(turn_angle)
            lock_behavior = False
    elif current_state_inner.lower() == 'l' and old_state_inner.lower() == 'r':
        if lock_behavior == True:
            reverse_move()
            lock_behavior = False
    elif current_state_inner.lower() == 'l' and old_state_inner.lower() == 'l':
        robot.drive(speed, 0)

    # # Current state down
    elif current_state_inner.lower() == 'd' and old_state_inner.lower() == 'u':
        if lock_behavior == True:
            reverse_move()
            lock_behavior = False
    elif current_state_inner.lower() == 'd' and old_state_inner.lower() == 'd':
        robot.drive(speed, 0)
    elif current_state_inner.lower() == 'd' and old_state_inner.lower() == 'r':
        if lock_behavior == True:
            turn_move(turn_angle)
            lock_behavior = False
    elif current_state_inner.lower() == 'd' and old_state_inner.lower() == 'l':
        if lock_behavior == True:
            turn_move(-turn_angle)
            lock_behavior = False

    # Current state up
    elif current_state_inner.lower() == 'u' and old_state_inner.lower() == 'u':
        robot.drive(speed, 0)
    elif current_state_inner.lower() == 'u' and old_state_inner.lower() == 'd':
        if lock_behavior == True:
            reverse_move()
            lock_behavior = False
    elif current_state_inner.lower() == 'u' and old_state_inner.lower() == 'r':
        if lock_behavior == True:
            turn_move(-turn_angle)
            lock_behavior = False
    elif current_state_inner.lower() == 'u' and old_state_inner.lower() == 'l':
        if lock_behavior == True:
            turn_move(turn_angle)
            lock_behavior = False

### Behavior ###
while True:
    snsRight = lineRight.reflection()
    snsMid = lineMid.reflection()
    snsLeft = lineLeft.reflection()

#     print('left: '+str(snsLeft))
#     print('mid: '+str(snsMid))
#     print('right: '+str(snsRight))

    if snsLeft > black and snsMid < black and snsRight > black:
        # Drive forward (mid sensor black)
        current_state = 'F'
    elif snsLeft < black and snsMid < black and snsRight > black:
        # Turn left (left and mid sensor black)
        if lock_states == True:
            old_state = states[0]
            current_state = states[1]
            states.pop(0)
            lock_states = False
    elif snsLeft > black and snsMid < black and snsRight < black:
        # Turn right (right and mid sensor black)
        if lock_states == True:
            old_state = states[0]
            current_state = states[1]
            states.pop(0)
            lock_states = False
    elif snsLeft < black and snsMid < black and snsRight < black:
        # All sensors black
        if lock_states == True:
            old_state = states[0]
            current_state = states[1]
            states.pop(0)
            lock_states = False
    
    print('old: '+old_state)
    print('Current: '+current_state)

    if current_state == 'F':
        robot.drive(speed,0)
        lock_states = True
        lock_behavior = True
    else:
        move_behavior(current_state,old_state)