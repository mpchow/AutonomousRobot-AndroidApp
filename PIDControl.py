

def Controller():
    OpticalValue = [0,0,0,0,0]
    Error = 0
    while True:
        OpticalValue = GETFROMSENSORS()
        Error = CalculateError(OpticalValue)


def CalculateError(OpticalValue):
    ErrorTotal = (OpticalValue[0] * 10000)
    ErrorTotal += (OpticalValue[1] * 1000)
    ErrorTotal += (OpticalValue[2] * 100)
    ErrorTotal += (OpticalValue[3] * 10)
    ErrorTotal += OpticalValue[4]

    if (ErrorTotal == 00001):
        Error = 4
    elif (ErrorTotal == 00011):
        Error = 3
    elif (ErrorTotal == 00010):
        Error = 2
    elif (ErrorTotal == 00110):
        Error = 1
    elif (ErrorTotal == 00100):
        Error = 0
    elif (ErrorTotal == 01100):
        Error = -1
    elif (ErrorTotal == 01000):
        Error = -2
    elif (ErrorTotal == 11000):
        Error = -3
    elif (ErrorTotal == 10000):
        Error = -4
    
    return Error
