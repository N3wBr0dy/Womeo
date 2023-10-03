import picamera
import ST7789
import numpy as np
import cv2
import time
from PIL import Image
from PIL import ImageOps
from io import BytesIO

# Initialize the Display-O-Tron HAT Mini display
disp = ST7789.ST7789(port=0, cs=1, dc=9, backlight=13, spi_speed_hz=10000000)

# Set up the camera
camera = picamera.PiCamera()
camera.resolution = (320, 240)

# Create a function for posterizing an image
def posterize(image, levels=4):
    img = ImageOps.posterize(image, levels)
    return img

try:
    while True:
        # Capture an image from the camera
        with BytesIO() as stream:
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            image = Image.open(stream)

        # Apply posterize effect
        posterized_image = posterize(image, levels=4)

        # Convert the posterized image to a numpy array
        posterized_np = np.array(posterized_image)

        # Resize the numpy array to match the display size (240x240)
        posterized_np = cv2.resize(posterized_np, (240, 240))

        # Display the posterized image on the Display-O-Tron HAT Mini
        disp.display(posterized_np)

except KeyboardInterrupt:
    # Clean up and close the display and camera when Ctrl+C is pressed
    disp.cleanup()
    camera.close()
