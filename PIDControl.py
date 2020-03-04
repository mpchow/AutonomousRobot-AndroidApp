from adafruit_motorkit import MotorKit



def controller():
    #Instantiate the motorkit instance
    kit = MotorKit()
    #Initially start the motors at same speed so they are running straight
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = 0.75
    #Instantiate the error class to calculate things for us
    error = Error()
    #Loop for the feedback loop
    while True:
        #Calculate the PID value
        PID = error.calculatePID()
        #summ the pid value with the base throttle of 0.75 to turn left or right based on imbalances in the throttle values
        kit.motor1.throttle = 0.75 + PID #Assuming this is the left motor 
        kit.motor2.throttle = 0.75 - PID #Assuming this is the right motor
 
class Error:
    def __init__(self):
        self.sensorVal = [0, 0, 0, 0, 0]
        self.error = 0
        self.prevError = 0
        self.integral = 0
        self.Kp = 0.0625
        self.Kd = 0
        self.Ki = 0
        
    
    def calculateError(self):
        #0 is the left sensor, 4 is the rightmost sensor from a topdown view
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
        self.calculateError()
        self.integral += self.error
        pidValue = self.Kp * self.error + self.Kd * (self.error - self.prevError) + self.Ki * self.integral
        self.prevError = self.error
        return pidValue