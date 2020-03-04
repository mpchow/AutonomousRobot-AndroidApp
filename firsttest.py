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