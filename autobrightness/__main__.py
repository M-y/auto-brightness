import webcam
import brightness
import config
import time

config = config.Config()
camera = webcam.Camera( config.camera )
display = brightness.Display( config.backend )

while True:
    ambient_brightness = camera.getBrightness()
    brightness = round( display.maxBrightness * ambient_brightness / 255 )

    display.setBrightness(brightness)

    if ( config.interval < 1 ):
        break
    time.sleep( config.interval )
