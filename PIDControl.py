from adafruit_motorkit import MotorKit

kit = MotorKit()
P = 0
I = 0
D = 0
error = 0
prevError = 0

def controller():
    opticalValue = [0, 0, 0, 0, 0]
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = 0.75
    prevError = 0

    while True:
        opticalValue = GETFROMSENSORS()
        PIDVal = calculatePID(opticalValue, prevError)

def calculatePID(opticalValue, prevError):

    error = calculateError(opticalValue)
    P = error
    I += error
    D = error - prevError
    prevError = error

class Error:
    def __init__(self):
        self.farLeft = 0
        self.midLeft = 0
        self.middle = 0
        self.midRight = 0
        self.farRight = 0
        self.error = 0
    
    def calculateError(self):
        errorTotal = (self.farLeft * 10000)
        errorTotal += (self.midLeft * 1000)
        errorTotal += (self.middle * 100)
        errorTotal += (self.midRight * 10)
        errorTotal += self.farRight

        if (errorTotal == 1):
            self.error = 4
        elif (errorTotal == 11):
            self.error = 3
        elif (errorTotal == 10):
            self.error = 2
        elif (errorTotal == 110):
            self.error = 1
        elif (errorTotal == 100):
            self.error = 0
        elif (errorTotal == 1100):
            self.error = -1
        elif (errorTotal == 1000):
            self.error = -2
        elif (errorTotal == 11000):
            self.error = -3
        elif (errorTotal == 10000):
            self.error = -4