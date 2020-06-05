from autobrightness import webcam
from autobrightness import brightness
from autobrightness import config
import time
import keyboard
import pkg_resources

version = pkg_resources.require("autobrightness")[0].version

config = config.Config()
camera = webcam.Camera( config.camera )
display = brightness.Display( config.backend )

def autobrightness():
    ambient_brightness = camera.getBrightness()
    brightness = round( display.maxBrightness * ambient_brightness / 255 )
    display.setBrightness(brightness)
    print("Set brightness to " + str(brightness))

def main():
    def hotkey(event):
        if event.scan_code == config.keycode and event.event_type == 'up':
            autobrightness()
    
    if config.keycode > 0:
        keyboard.hook(hotkey)

    while True:
        if config.interval > 0:
            time.sleep( config.interval )
            autobrightness()
        elif config.keycode > 0:
            time.sleep(1)
        else:
            break

if __name__ == "__main__":
    main()