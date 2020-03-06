#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

# Write some Text

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale = 1
fontColorBright = (255,255,255)
fontColorDark = (0,0,0)
lineType = 2

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    #lower threshold, upper color threshold
    brightmask = cv2.inRange(image, (245,245,245), (255,255,255))
    darkmask = cv2.inRange(image, (0,0,0), (10,10,10))

    brightBits = cv2.countNonZero(brightmask)
    darkBits = cv2.countNonZero(darkmask)

    cv2.imshow("Frame", image)
    cv2.imshow("BrightMask", brightmask)
    cv2.imshow("DarkMask", darkmask)

    x = 640/2
    y = 480/2

    if brightBits > 640*480*0.9:
        cv2.putText(image, "Too Bright", (x, y), cv2.CV_FONT_HERSHEY_SIMPLEX, thickness=2, color=255)
        cv2.putText(image, "Too Bright", (x, y), cv2.CV_FONT_HERSHEY_SIMPLEX, thickness=3, color=0)

    if darkBits > 640 * 480 * 0.9:
        cv2.putText(image, "Too Dark", (x, y), cv2.CV_FONT_HERSHEY_SIMPLEX, thickness=2, color=255)
        cv2.putText(image, "Too Dark", (x, y), cv2.CV_FONT_HERSHEY_SIMPLEX, thickness=3, color=0)

    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        cv2.destroyAllWindows()
        break

