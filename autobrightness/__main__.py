from autobrightness import webcam
from autobrightness import brightness
from autobrightness import config
import time
import keyboard
import pkg_resources
import gettext
import os

version = pkg_resources.require("autobrightness")[0].version
config = config.Config()

if config.language is None:
    lang = gettext
else:
    lang = gettext.translation("autobrightness", pkg_resources.resource_filename('autobrightness', 'locales'), [config.language])
_ = lang.gettext

camera = webcam.Camera( config.camera )
display = brightness.Display( config.backend )

def autobrightness():
    ambient_brightness = camera.getBrightness()
    brightness = round( display.maxBrightness * ambient_brightness / 255 )
    display.setBrightness(brightness)
    print(_("Adjust brightness to %d") % brightness)

def main():
    def shortcut(e = None):
        autobrightness()

    if not config.shortcut is None:
        if type(config.shortcut) == str:
            keyboard.add_hotkey(config.shortcut, shortcut)
        else:
            keyboard.on_press_key(config.shortcut, shortcut)

    while True:
        if config.interval > 0:
            time.sleep( config.interval )
            autobrightness()
        elif not config.shortcut is None:
            time.sleep(1)
        else:
            break

if __name__ == "__main__":
    main()
