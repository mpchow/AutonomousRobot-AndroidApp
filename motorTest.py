"""Simple test for using adafruit_motorkit with a DC motor"""
from time import sleep
from adafruit_motorkit import MotorKit
import PIDControl

kit = MotorKit()

# Function for robot to go straight
def straight():
    kit.motor1.throttle = .25
    kit.motor2.throttle = .25
    sleep(1)
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

# Function for robot to turn left
def turnLeft():
    kit.motor1.throttle = 0.25
    kit.motor2.throttle = 0.5
    sleep(1)
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

# Function for robot to turn right
def turnRight():
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 0.25
    sleep(1)
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

def off():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    sleep(1)
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

try:
    while True:
        print("Straight")
        straight()
        sleep(2)
        print("Left")
        turnLeft()
        sleep(2)
        print("Right")
        turnRight()
        sleep(2)
        off()
        sleep(2)

except KeyboardInterrupt:
    off()

#comment out if you want
try:
    PIDControl.controller()
except KeyboardInterrupt:
    off()