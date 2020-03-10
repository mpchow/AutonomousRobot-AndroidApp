from RPi import GPIO
from adafruit_motorkit import MotorKit
import digitalio
import board
import time

GPIO.setmode(GPIO.BCM)

# Assign sensor pins
sensor1 = 26
sensor2 = 19
sensor3 = 13
# Setup GPIO inputs
GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)


def controller():
    #Instantiate the motorkit instance
    kit = MotorKit()
    #Initially start the motors at same speed so they are running straight
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    #Instantiate the error class to calculate things for us
    error = Error()
    #Loop for the feedback loop
    try:
        while True:
            #Calculate the PID value
            error.getOptics()
            PID = error.calculatePID()
            if (error.count == 22):
                kit.motor1.throttle = 0.0
                kit.motor2.throttle = 0.0
                break
            time.sleep(0.05)
            #summ the pid value with the base throttle of 0.75 to turn left or right based on imbalances in the throttle values
            kit.motor1.throttle = 0.27 + PID #Assuming this is the left motor
            kit.motor2.throttle = 0.27 - PID #Assuming this is the right motor

    except KeyboardInterrupt:
        kit.motor1.throttle = 0.0
        kit.motor2.throttle = 0.0

class Error:
    def __init__(self):
        # sensorVal[0] = left, sensorVal[1] = middle, sensorVal[2] = right
        self.sensorVal = [0, 0, 0]
        self.error = 0
        self.prevError = 0
        self.integral = 0
        self.Kp = 0.07
        self.Kd = 0.13
        self.Ki = 0
        self.count = 0


    def calculateError(self):
        # 0th index is for left sensor, 4th is the rightmost sensor from a topdown view
        # Shift array elements to create one sum
        errorTotal = (self.sensorVal[0] * 100)
        errorTotal += (self.sensorVal[1] * 10)
        errorTotal += self.sensorVal[2]

        if (errorTotal == 1):           # right sensor triggered
            self.count = 0
            self.error = -2
        elif (errorTotal == 11):        # middle and right sensors triggered
            self.count = 0
            self.error = -1
        elif (errorTotal == 10):        # middle sensor triggered
            self.count = 0
            self.error = 0
        elif (errorTotal == 110):       # middle and left sensors triggered
            self.count = 0
            self.error = 1
        elif (errorTotal == 100):       # left sensor triggered
            self.count = 0
            self.error = 2
        elif (errorTotal == 111):       # all sensors triggered, most likely crossover
            self.count = 0
            self.error = 0
        elif (errorTotal == 0):
            self.count = self.count + 1


    def getOptics(self):
        sens1 = GPIO.input(sensor1)
        sens2 = GPIO.input(sensor2)
        sens3 = GPIO.input(sensor3)
        self.sensorVal = [sens1, sens2, sens3]


    def calculatePID(self):
        # Calculates PID value based on new sensor inputs and past values (prevError, integral)
        self.calculateError()           # adjust error values based on sensor readings
        self.integral += self.error
        pidValue = self.Kp * self.error + self.Kd * (self.error - self.prevError) + self.Ki * self.integral
        self.prevError = self.error     # set prevError to new error for next iteration
        return pidValue

controller()