from RPi import GPIO
from time import sleep

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont

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

# Function to get optical sensor outputs, store in array and return
def getOptics():
	sens1 = GPIO.input(sensor1)
	sens2 = GPIO.input(sensor2)
	sens3 = GPIO.input(sensor3)
	sens4 = GPIO.input(sensor4)
	sens5 = GPIO.input(sensor5)
	opArr = [sens1, sens2, sens3, sens4, sens5]
	return opArr

try:
    while True:
        sensArr = getOptics()
        for x in sensArr:
            print(x)
        sleep(2)
except KeyboardInterrupt:
	GPIO.cleanup()