import ST7789
import picamera
import picamera.array
import time
import numpy as np

# Initialize the Display-O-Tron HAT Mini
disp = ST7789.ST7789(
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=10000000,
    width=160,
    height=120
)
disp.begin()

# Initialize the PiCamera
camera = picamera.PiCamera()
camera.resolution = (160, 120)
camera.framerate = 60
camera.rotation = 270  # Rotate the image 90 degrees clockwise

# Start the preview and display it on the Display-O-Tron HAT Mini
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
        
        # Set the window size and position for the image
        x_offset = (disp.width - posterised_image.shape[1]) // 2
        y_offset = (disp.height - posterised_image.shape[0]) // 2
        disp.set_window(x_offset, y_offset, posterised_image.shape[1], posterised_image.shape[0])
        
        # Display the posterised image on the Display-O-Tron HAT Mini
        disp.display(posterised_image)
        
        # Wait for the next frame
        time.sleep(0.001)
finally:
    camera.stop_preview()
