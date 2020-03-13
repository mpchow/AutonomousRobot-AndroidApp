from picamera import PiCamera
from time import sleep
import io
import socket
import struct
import time
import picamera
from PIL import Image
# from adafruit_st7735r import ST7735R
# import adafruit_imageload

PORT = 5017       # Port to listen on (non-privileged ports are > 1023)
HOST = ''

camera = PiCamera()

# Reference for sending stream: https://picamera.readthedocs.io/en/release-1.10/recipes1.html
def captureStreamPIL():
    stream = io.BytesIO()                   
    camera.capture(stream, format='bmp')    # capture the image and store in stream as bmp
    stream.seek(0)                          # start at beginning of stream 
    image = Image.open(stream)              # read the contents of the stream and store in PIL Image

    # Convert to byte array 
    imgByteArr = io.BytesIO()               
    image.save(imgByteArr, format='bmp')
    imgByteArrToReturn = imgByteArr.getvalue()

    # Return to byte array to send 
    return imgByteArrToReturn


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    (conn, addr) = s.accept()
    print("Connected")
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    while True:
        img = captureStreamPIL()
        conn.send(img)

    camera.stop_preview()
    s.close()




