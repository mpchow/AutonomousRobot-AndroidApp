from RPi import GPIO
from adafruit_motorkit import MotorKit
import time
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
import socket

PORT = 5023      # Port to listen on (non-privileged ports are > 1023)
HOST = ''

GPIO.setmode(GPIO.BCM)

# Assign sensor pins
sensor1 = 26
sensor2 = 19
sensor3 = 13

# Setup GPIO inputs
GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()
# 1.44" ST7735R
disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

class Error:
    def __init__(self):
        # sensorVal[0] = left, sensorVal[1] = middle, sensorVal[2] = right
        self.sensorVal = [0, 0, 0]
        self.error = 0
        self.prevError = 0
        self.integral = 0
        self.Kp = 0.08
        self.Kd = 0.13
        self.Ki = 0
        # count for stopping motors
        self.count = 0


    def calculateError(self):
        # 0th index is for left sensor, 4th is the rightmost sensor from a topdown view
        # Shift array elements to create one sum
        errorTotal = (self.sensorVal[0] * 100)
        errorTotal += (self.sensorVal[1] * 10)
        errorTotal += self.sensorVal[2]

        if (errorTotal == 1):           # right sensor triggered
            self.count = 0
            self.error = -1.5
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
            self.error = 1.5
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

#Instantiate the error class to calculate things for us
error = Error()

# Function to parse json
def parseJson(byteStream):
    # Decode UTF-8 bytes to unicode
    # To make valid JSON, replace single quotes with double quotes
    jsonStream = byteStream.decode('utf8').replace("'", '"')
    # Load JSON to Python list
    jsonObject = json.loads(jsonStream)
    print(jsonObject)
    print(jsonObject.get("Type"))
    return jsonObject

# Function for robot to go straight
def straight(kit):
    kit.motor1.throttle = 0.40
    kit.motor2.throttle = 0.40

# Function for robot to turn left
def turnLeft(kit):
    kit.motor1.throttle = 0.25
    kit.motor2.throttle = 0.5

# Function for robot to turn right
def turnRight(kit):
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 0.25

def off(kit):
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

#parameter is the imageName to write to board
def writeImages(imageName):
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

def controller(kit):
    global error

    #Loop for the feedback loop
    try:
        #Calculate the PID value
        error.getOptics()
        PID = error.calculatePID()
        time.sleep(0.02)

        # Print stop image if counted to 25
        if (error.count == 25):
            writeImages("stopGear.jpg")
            kit.motor1.throttle = 0.0
            kit.motor2.throttle = 0.0
        elif (PID == 0.0):
            kit.motor1.throttle = 0.40
            kit.motor2.throttle = 0.40
            #sum the pid value with the base throttle of 0.75 to turn left or right based on imbalances in the throttle values
        else :
            kit.motor1.throttle = 0.25 + PID #Assuming this is the left motor
            kit.motor2.throttle = 0.25 - PID #Assuming this is the right motor

    except KeyboardInterrupt:
        kit.motor1.throttle = 0.0
        kit.motor2.throttle = 0.0


#Instantiate the motorkit instance
kit = MotorKit()

# Wait for client connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    off(kit)
    s.bind((HOST, PORT))
    s.listen()
    (conn, addr) = s.accept()
    print("Connected")
    with conn:
        print('Connected by', addr)
        input = conn.recv(1024)
        noValue = input
        conn.setblocking(0)
        mode = "Autonomous"

        # Once connected, continuously check for input from app
        while True:
            try:
                input = conn.recv(1024)
            except:
                print("Yeet")

            print(input)
            if input != noValue:
                print("Trying to print")
                parseJson(input)
                jsonObj = parseJson(input)
                mode = jsonObj.get('Mode')

            if (mode == 'Autonomous'):
                controller(kit)
            elif (mode == 'Remote Control'):
                Type = jsonObj.get("Type")
                if (Type == 'Forward'):
                    straight(kit)
                elif (Type == 'Left'):
                    turnLeft(kit)
                elif (Type == 'Right'):
                    turnRight(kit)
                else:
                    off(kit)
            else:
                off(kit)

        s.close()