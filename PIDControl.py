from adafruit_motorkit import MotorKit

kit = MotorKit()

def controller():
    opticalValue = [0, 0, 0, 0, 0]
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = 0.75
    prevError = 0
    error = Error()
    while True:
        PID = error.calculatePID()

        kit.motor1.throttle = 0.75 + PID #Assuming this is the left motor 
        kit.motor2.throttle = 0.75 - PID #Assuming this is the right motor
 
class Error:
    def __init__(self):
        # sensorVal[0] = far left, sensorVal[1] = mid left, sensorVal[2] = middle
        # sensorVal[3] = mid right, sensorVal[4] = far right
        self.sensorVal = [0, 0, 0, 0, 0]
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