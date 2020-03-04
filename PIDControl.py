from adafruit_motorkit import MotorKit

kit = MotorKit()

def controller():
    opticalValue = [0, 0, 0, 0, 0]
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = 0.75
    prevError = 0
    error = Error()
    while True:
        opticalValue = GETFROMSENSORS()
        PIDVal = calculatePID(opticalValue, prevError)
        kit.motor1.throttle = 0.75 +
        kit.motor2.throttle = 0.75 +

class Error:
    def __init__(self):
        self.sensorVal = [0, 0, 0, 0, 0]
        self.error = 0
        self.prevError = 0
        self.integral = 0
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        
    
    def calculateError(self):
        errorTotal = (self.sensorVal[0] * 10000)
        errorTotal += (self.sensorVal[1] * 1000)
        errorTotal += (self.sensorVal[2] * 100)
        errorTotal += (self.sensorVal[3] * 10)
        errorTotal += self.sensorVal[4]

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

    def calculatePID(self):
        error = self.calculateError()
        self.integral += error
        pidValue = self.Kp * error + self.Kd * (error - self.prevError) + self.Ki * self.integral
        self.prevError = error
        return pidValue