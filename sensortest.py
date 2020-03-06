from RPi import GPIO
from time import sleep

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_motorkit import MotorKit

GPIO.setmode(GPIO.BCM)

# Assign sensor pins
sensor1 = 5
sensor2 = 6
sensor3 = 13
sensor4 = 19
sensor5 = 26

GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)
GPIO.setup(sensor4, GPIO.IN)
GPIO.setup(sensor5, GPIO.IN)

while True:
    print("One Val: ", GPIO.input(sensor5))
    print("Two Val: ", GPIO.input(sensor4))
    print("Three Val: ", GPIO.input(sensor3))
    print("Four Val: ", GPIO.input(sensor2))
    print("Five Val: ", GPIO.input(sensor1))
    sleep(2)