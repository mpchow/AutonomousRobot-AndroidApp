from RPi import GPIO
from time import sleep

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_motorkit import MotorKit

GPIO.setmode(GPIO.BCM)

# Assign sensor pins
sensor1 = 26
sensor2 = 19
sensor3 = 13

GPIO.setup(sensor1, GPIO.IN) # set up GPIO 1
GPIO.setup(sensor2, GPIO.IN) # set up GPIO 2
GPIO.setup(sensor3, GPIO.IN) # set up GPIO 3
while True:
    print("One Val: ", GPIO.input(sensor1)) # print sensor 1 value
    print("Two Val: ", GPIO.input(sensor2)) # print sensor 2 value
    print("Three Val: ", GPIO.input(sensor3)) # print sensor 3 value
    sleep(2) # sleep for 2 seconds