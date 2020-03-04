"""Simple test for using adafruit_motorkit with a DC motor"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

kit.motor1.throttle = 1.0
time.sleep(1.0)
kit.motor1.throttle = 0
kit.motor2.throttle =1.0
time.sleep(1.0)
kit.motor2.throttle = 0

# Function for robot to go straight
def straight():
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = 1.0

# Function for robot to turn left 
def turnLeft():
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 1.0

# Function for robot to turn right
def turnRight():
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = 0.5

# Function for robot to go backwards 
def backwards():
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = -1.0

