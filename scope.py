import picamera
import ST7789
import numpy as np
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
    posterized_image = ImageOps.posterize(image, levels)
    return posterized_image

try:
    while True:
        # Capture an image from the camera
        with BytesIO() as stream:
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            image = Image.open(stream)

        # Apply posterize effect
        posterized_image = posterize(image, levels=4)

        # Resize the posterized image to fit the display
        posterized_image = posterized_image.resize((240, 240), Image.ANTIALIAS)

        # Convert the posterized image to a numpy array
        posterized_np = np.array(posterized_image)

        # Display the posterized image on the Display-O-Tron HAT Mini
        disp.display(posterized_np)

except KeyboardInterrupt:
    # Clean up and close the display and camera when Ctrl+C is pressed
    disp.cleanup()
    camera.close()
