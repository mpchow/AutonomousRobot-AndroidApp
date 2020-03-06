#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    image_red = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #change from bgr to hsv

    #lower threshold, upper color threshold
    brightmask = cv2.inRange(image, (245,245,245), (255,255,255))
    darkmask = cv2.inRange(image, (0,0,0), (10,10,10))
    redmask = cv2.inRange(image_red, (160,100,100),(179,255,255))

    brightBits = cv2.countNonZero(brightmask)
    darkBits = cv2.countNonZero(darkmask)
    redBits = cv2.countNonZero(redmask)

    if brightBits > 640 * 480 * 0.9:
        print("Too Bright")

    if darkBits > 640 * 480 * 0.9:
        print("Too Dark")

    if redBits > 640 * 480 * 0.2:
        print("Too Red")

    cv2.imshow("Frame", image)
    cv2.imshow("BrightMask", brightmask)
    cv2.imshow("DarkMask", darkmask)
    cv2.imshow("RedMask", redmask)

    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        cv2.destroyAllWindows()
        break
