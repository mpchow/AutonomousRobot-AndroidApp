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
        kit.motor1.throttle = 0.75 +
        kit.motor2.throttle = 0.75 +

def calculatePID(opticalValue, prevError):

    error = calculateError(opticalValue)
    integral += error
    prevError = error

    return (Kp * error )+ (Kd * (error - prevError)) + (Ki * integral)



def calculateError(opticalValue):
    errorTotal = (opticalValue[0] * 10000)
    errorTotal += (opticalValue[1] * 1000)
    errorTotal += (opticalValue[2] * 100)
    errorTotal += (opticalValue[3] * 10)
    errorTotal += opticalValue[4]

    if (errorTotal == 1):
        error = 4
    elif (errorTotal == 11):
        error = 3
    elif (errorTotal == 10):
        error = 2
    elif (errorTotal == 110):
        error = 1
    elif (errorTotal == 100):
        error = 0
    elif (errorTotal == 1100):
        error = -1
    elif (errorTotal == 1000):
        error = -2
    elif (errorTotal == 11000):
        error = -3
    elif (errorTotal == 10000):
        error = -4
    
    return error
