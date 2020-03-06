from RPi import GPIO
from adafruit_motorkit import MotorKit
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789        # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357        # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735        # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351      # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331      # pylint: disable=unused-import

import json

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

count = 0

#parameter is the imageName to write to board
def writeImages(imageName):
    # Configuration for CS and DC pins (these are PiTFT defaults):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 24000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()
    disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
                           cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
    # pylint: enable=line-too-long

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width   # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width   # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new('RGB', (width, height))
 
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
 
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0)) # create a rectangle that is blank to put on the LCD
    disp.image(image) # put the image on the LCD
    
    image = Image.open(imageName) # open the image given by the string imageName
    
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
 
    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
 
    # Display image.
    disp.image(image)

def animation():
    global count
    # show animation by iterating through 3 similar images
    if (count == 1):
        writeImages("firstGear.jpg")
    elif (count == 2):
        writeImages("secondGear.jpg")
    else:
        writeImages("thirdImg.jpg")
        count = 0


def parseJson(inputStream):
    data = json.load(inputStream)
        writeImages("thirdGear.jpg")
        count = 0   # return to first image
        
def controller():
    global count
    #Instantiate the motorkit instance
    kit = MotorKit()
    #Initially start the motors at same speed so they are running straight
    kit.motor1.throttle = 0.25
    kit.motor2.throttle = 0.25
    #Instantiate the error class for calculations
    error = Error()
    #Loop for the feedback loop
    try:
        while True:
            #Calculate the PID value
            error.getOptics()
            PID = error.calculatePID()

            # If PID is less than threshold, robot turn right
            if (PID < -28):
                writeImages("rightArrow.jpg")

            # If PID greater than threshold, robot turn left
            elif(PID > 28):
                writeImages("leftArrow.jpg")
            
            # If robot going straight or performing negligble turns, play animation
            else:
                count += 1
                animation()

            #sum the pid value with the base throttle of 0.75 to turn left or right based on imbalances in the throttle values
            kit.motor1.throttle = 0.25 + PID #Assuming this is the left motor
            kit.motor2.throttle = 0.25 - PID #Assuming this is the right motor

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
        self.Kp = 0.0005
        self.Kd = 0
        self.Ki = 0

    def calculateError(self):
        # 0th index is for left sensor, 4th is the rightmost sensor from a topdown view
        # Shift array elements to create one sum
        errorTotal = (self.sensorVal[0] * 100)
        errorTotal += (self.sensorVal[1] * 10)
        errorTotal += self.sensorVal[2] 

        if (errorTotal == 1):           # right sensor triggered
            self.error = -4
        elif (errorTotal == 11):        # middle and right sensors triggered
            self.error = -1
        elif (errorTotal == 10):        # middle sensor triggered
            self.error = 0
        elif (errorTotal == 110):       # middle and left sensors triggered
            self.error = 1
        elif (errorTotal == 100):       # left sensor triggered
            self.error = 4

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