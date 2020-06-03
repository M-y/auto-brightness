from autobrightness import webcam
from autobrightness import brightness
from autobrightness import config
import time

with open('autobrightness/VERSION') as version_file:
    version = version_file.read().strip()

config = config.Config()
camera = webcam.Camera( config.camera )
display = brightness.Display( config.backend )

def main():
    while True:
        ambient_brightness = camera.getBrightness()
        brightness = round( display.maxBrightness * ambient_brightness / 255 )

        display.setBrightness(brightness)

        if ( config.interval < 1 ):
            break
        time.sleep( config.interval )

if __name__ == "__main__":
    main()