from RPi import GPIO
from time import sleep

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_motorkit import MotorKit

GPIO.setmode(GPIO.BCM)

# Assign sensor pins
sensor1 = 5
sensor2 = 6
sensor3 = 13
sensor4 = 19
sensor5 = 26

# Setup GPIO inputs
GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)
GPIO.setup(sensor4, GPIO.IN)
GPIO.setup(sensor5, GPIO.IN)

errorObj = Error()

class Error:
    def __init__(self):
        # sensorVal[0] = far left, sensorVal[1] = mid left, sensorVal[2] = middle
        # sensorVal[3] = mid right, sensorVal[4] = far right
        # setting up the class values
        self.sensorVal = [0, 0, 0, 0, 0] # sensor value arrays
        self.error = 0
        self.prevError = 0
        self.integral = 0
        self.Kp = 0.0625
        self.Kd = 0
        self.Ki = 0


    def calculateError(self):
        # 0th index is for left sensor, 4th is the rightmost sensor from a topdown view
        # Shift array elements to create one sum
        errorTotal = (self.sensorVal[0] * 10000)
        errorTotal += (self.sensorVal[1] * 1000)
        errorTotal += (self.sensorVal[2] * 100)
        errorTotal += (self.sensorVal[3] * 10)
        errorTotal += self.sensorVal[4]

        if (errorTotal == 1):           # far right sensor triggered
            self.error = 4
        elif (errorTotal == 11):        # far & mid right sensors triggered
            self.error = 3
        elif (errorTotal == 10):        # mid right sensor triggered
            self.error = 2
        elif (errorTotal == 110):       # middle & mid right sensors triggered
            self.error = 1
        elif (errorTotal == 100):       # middle sensor triggered
            self.error = 0
        elif (errorTotal == 1100):      # middle & mid left sensors triggered
            self.error = -1
        elif (errorTotal == 1000):      # mid left sensor triggered
            self.error = -2
        elif (errorTotal == 11000):     # far & mid left sensors triggered
            self.error = -3
        elif (errorTotal == 10000):     # far left sensor triggered
            self.error = -4

    def calculatePID(self):
        # Calculates PID value based on new sensor inputs and past values (prevError, integral)
        self.calculateError()           # adjust error values based on sensor readings
        self.integral += self.error
        pidValue = self.Kp * self.error + self.Kd * (self.error - self.prevError) + self.Ki * self.integral
        self.prevError = self.error     # set prevError to new error for next iteration
        return pidValue

def controller():
	global errorObj
    #Instantiate the motorkit instance
    kit = MotorKit()
	#Initially start the motors at same speed so they are running straight
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = 0.75
    #Instantiate the error class to calculate things for us

    #Loop for the feedback loop
    while True:
        #Calculate the PID value
        PID = errorObj.calculatePID()
        #summ the pid value with the base throttle of 0.75 to turn left or right based on imbalances in the throttle values
        kit.motor1.throttle = 0.75 + PID
        kit.motor2.throttle = 0.75 - PID

# Function to get optical sensor outputs, store in array and returnz
def getOptics():
	global errorObj
	sens1 = GPIO.input(sensor1) # get sensor 1 value
	sens2 = GPIO.input(sensor2) # get sensor 2 value
	sens3 = GPIO.input(sensor3) # get sensor 3 value
	sens4 = GPIO.input(sensor4) # get sensor 4 value
	sens5 = GPIO.input(sensor5) # get sensor 5 value
	errorObj.sensorVal = [sens1, sens2, sens3, sens4, sens5] # put all sensor values into the sensor array
	
try:
    while True:
        sensArr = getOptics()
        for x in sensArr:
            print(x)
        sleep(2)
except KeyboardInterrupt:
	GPIO.cleanup()