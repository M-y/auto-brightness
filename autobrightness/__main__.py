from autobrightness import webcam
from autobrightness import brightness
from autobrightness import config
import time
import keyboard
import pkg_resources
import gettext
import os
import argparse

version = pkg_resources.require("autobrightness")[0].version
config = config.Config()

# select language
if config.language is None:
    lang = gettext
else:
    lang = gettext.translation("autobrightness", pkg_resources.resource_filename('autobrightness', 'locales'), [config.language])
_ = lang.gettext

def init_argparse() -> argparse.ArgumentParser:
    """
    init command line arguments
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description=_("Auto change screen brightness using webcam.")
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version {version}"
    )

    parser.add_argument("--start", help=_("Start the daemon"), action='store_true')
    parser.add_argument("--set", help=_("Set brightness and exit"), action='store_true')

    return parser

def autobrightness(camera, display):
    """
    Calculate and sets brightness

    Parameters:
        camera (object)
        display (object)
    """
    ambient_brightness = camera.getBrightness()
    calculated = round( display.maxBrightness * ambient_brightness / 255 )

    print(_("Adjusting brightness to %(percentage)d%% (%(value)d)") % {'percentage': (calculated * 100 / display.maxBrightness), 'value': calculated})
    display.setBrightness(calculated)

def main():
    camera = webcam.Camera( config.camera )
    display = brightness.Display( config.backend )
    parser = init_argparse()
    args = parser.parse_args()
    
    if args.start:
        print(_("Starting daemon..."))

        def shortcut(e = None):
            print(_("Shortcut key used."))
            autobrightness(camera, display)

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
                print(_("No interval nor shortcut selected. Exiting."))
                break
    elif args.set:
        autobrightness(camera, display)
    else:
        print("will show config screen")

if __name__ == "__main__":
    main()
