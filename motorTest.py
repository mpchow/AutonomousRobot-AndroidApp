"""Simple test for using adafruit_motorkit with a DC motor"""
from time import sleep
from adafruit_motorkit import MotorKit
import PIDControl

kit = MotorKit()

# Function for robot to go straight
def straight():
    kit.motor1.throttle = .25 # set left motor speed
    kit.motor2.throttle = .25 # set right motor speed
    sleep(1) # sleep for 1 second
    kit.motor1.throttle = 0 # set left motor speed
    kit.motor2.throttle = 0 # set right motor speed

# Function for robot to turn left
def turnLeft():
    kit.motor1.throttle = 0.25 # set left motor speed
    kit.motor2.throttle = 0.5 # set right motor speed
    sleep(1) # sleep for 1 second
    kit.motor1.throttle = 0 # set left motor speed
    kit.motor2.throttle = 0 # set right motor speed

# Function for robot to turn right
def turnRight():
    kit.motor1.throttle = 0.5 # set left motor speed
    kit.motor2.throttle = 0.25 # set right motor speed
    sleep(1) # sleep for 1 second
    kit.motor1.throttle = 0 # set left motor speed
    kit.motor2.throttle = 0 # set right motor speed

def off():
    kit.motor1.throttle = 0.0 # set left motor speed
    kit.motor2.throttle = 0.0 # set right motor speed
    sleep(1) # sleep for 1 second
    kit.motor1.throttle = 0 # set left motor speed
    kit.motor2.throttle = 0 # set right motor speed

try:
    while True:
        # while loop to test the app straight, left and right functions
        print("Straight")
        straight() # call straight function
        sleep(2) # sleep 2 seconds
        print("Left")
        turnLeft() # call left function
        sleep(2) # sleep 2 seconds
        print("Right")
        turnRight() # call right function
        sleep(2) # sleep 2 seconds
        off() # call function to turn off robot
        sleep(2) # sleep 2 seconds

except KeyboardInterrupt:
    off() # if keyboard interupt is detected turn off robot

#comment out if you want
try:
    PIDControl.controller()
except KeyboardInterrupt:
    off() # if keyboard interupt happens turn everything off