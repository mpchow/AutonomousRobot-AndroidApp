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

GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)
while True:
    print("One Val: ", GPIO.input(sensor1))
    print("Two Val: ", GPIO.input(sensor2))
    print("Three Val: ", GPIO.input(sensor3))
    sleep(2)