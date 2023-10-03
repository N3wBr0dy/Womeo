import ST7789
import picamera
import picamera.array
import time
import numpy as np
from PIL import Image

# Initialize the Display-O-Tron HAT Mini
disp = ST7789.ST7789(
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=10000000,
    width=320,
    height=240
)
disp.begin()

# Initialize the PiCamera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 60
camera.rotation = 270  # Rotate the image 90 degrees clockwise

# Start the preview and display it on the Display-O-Tron HAT Mini
camera.start_preview()
time.sleep(2)  # Wait for the camera to initialize

try:
    while True:
        # Capture a frame from the camera as a NumPy array
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='rgb', use_video_port=True)
            image = stream.array

        # Apply the "posterise" effect to the image
        posterised_image = np.array(np.round(image / 64) * 64, dtype=np.uint8)

        # Calculate the scaling factors for width and height to fit within the 320x240 display
        scale_width = 320 / posterised_image.shape[1]
        scale_height = 240 / posterised_image.shape[0]

        # Use the minimum of the two scaling factors to maintain aspect ratio
        scale = min(scale_width, scale_height)

        # Resize the image while maintaining its aspect ratio
        new_width = int(posterised_image.shape[1] * scale)
        new_height = int(posterised_image.shape[0] * scale)
        resized_image = Image.fromarray(posterised_image).resize((new_width, new_height))

        # Calculate the position to center the resized image on the 320x240 display
        x_offset = (320 - new_width) // 2
        y_offset = (240 - new_height) // 2

        # Convert the resized image back to a NumPy array
        resized_image = np.array(resized_image, dtype=np.uint8)

        # Set the window size and position for the centered and resized image
        disp.set_window(x_offset, y_offset, new_width, new_height)

        # Display the centered and resized posterised image on the Display-O-Tron HAT Mini
        disp.display(resized_image)

        # Wait for the next frame
        time.sleep(0.001)

finally:
    camera.stop_preview()
