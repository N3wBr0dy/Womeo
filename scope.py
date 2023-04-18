import ST7789
import picamera
import picamera.array
import time
import numpy as np

# Initialize the Display
disp = ST7789.ST7789(
    width=320,
    height=240,
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=10000000,
)
disp.begin()

# Initialize the PiCamera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

# Start the preview and display it on the Display
camera.start_preview()
time.sleep(2) # Wait for the camera to initialize
try:
    while True:
        # Capture a frame from the camera as a NumPy array
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='rgb', use_video_port=True)
            image = stream.array
            
        # Apply the "posterise" effect to the image
        posterised_image = np.array(np.round(image / 64) * 64, dtype=np.uint8)
        
        # Display the posterised image on the Display
        disp.display(posterised_image)
        
        # Wait for the next frame
        time.sleep(0.01)
finally:
    camera.stop_preview()
