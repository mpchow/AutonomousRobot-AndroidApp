from RPi import GPIO
from time import sleep

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789        # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357        # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735        # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351      # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331      # pylint: disable=unused-import

# First define some constants to allow easy resizing of shapes.
BORDER = 5
FONTSIZE = 24

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

# Draw a green filled box as the background
draw.rectangle((0, 0, width, height), fill=(0, 255, 0))
disp.image(image)

# Draw a smaller inner purple rectangle
draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1),
               fill=(170, 0, 136))

# Load a TTF Font
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', FONTSIZE)


GPIO.setmode(GPIO.BCM)

left_sensor = 11
right_sensor = 9

GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

try:
	while True:
		if not GPIO.input(left_sensor):
			print("Robot is straying off to the right, move left captain!")
			# Draw Some Text
			text = "Move Left!"
			(font_width, font_height) = font.getsize(text)
			draw.text((width//2 - font_width//2, height//2 - font_height//2),
          				text, font=font, fill=(255, 255, 0))

			# Display image.
			disp.image(image)

		elif not GPIO.input(right_sensor):
			print("Robot is straying off to the left, move right captain!")
			text = "Move Right!"
			(font_width, font_height) = font.getsize(text)
			draw.text((width//2 - font_width//2, height//2 - font_height//2),
          				text, font=font, fill=(255, 255, 0))

			# Display image.
			disp.image(image)
		else:
			print("Straight!")
			print("Robot is straying off to the left, move right captain!")
			text = "Move Right!"
			(font_width, font_height) = font.getsize(text)
			draw.text((width//2 - font_width//2, height//2 - font_height//2),
          				text, font=font, fill=(255, 255, 0))

			# Display image.
			disp.image(image)
			
		sleep(0.2)
except:
	GPIO.cleanup()