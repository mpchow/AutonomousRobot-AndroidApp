from picamera import PiCamera
from time import sleep
# from adafruit_st7735r import ST7735R
# import adafruit_imageload

camera = PiCamera()

# opens camera preview 
# unable to see if using remote access like SSH or VNC
camera.start_preview()
sleep(5)                                                # must sleep for at least 2 seconds so can sense light levels
camera.capture('/home/pi/Desktop/image.bmp', resize=(128, 128))
# displayImg()
camera.stop_preview()

def takePicture(imageName):
    







# make preview slightly see through so we can see errors
# camera.start_preview(alpha=200)

# Display image on the LCD
def displayImg(fileName):
    # Loads the bitmap image
    bitmap, palette = adafruit_imageload.load(fileName, bitmap=displayio.Bitmap, palette=displayio.Palette)
    # Create a TileGrid to store the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    # Create a Group to store the TileGrid
    group = displayio.Group()
    # Add the titleGrid to the Group
    group.append(tile_grid)
    # Show the group
    display.show(group)

def record():
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/testvid.h264')
    sleep(5)
    camera.stop_recording()
    camera.stop_preview()
