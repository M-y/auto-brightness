from autobrightness import webcam, brightness, config, gui
import time
import keyboard
import pkg_resources
import gettext
import os
import argparse

version = pkg_resources.require("autobrightness")[0].version

def init_argparse() -> argparse.ArgumentParser:
    """
    init command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Auto change screen brightness using webcam."
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version {version}"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--start", help="Start the daemon", action='store_true')
    group.add_argument("--set", help="Set brightness and exit", action='store_true')
    parser.add_argument("--config", help="Use alternative config file instead of .autobrightness in home directory.")

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
    parser = init_argparse()
    args = parser.parse_args()
    
    if args.config:
        settings = config.Config(args.config)
        settings.save()
    else:
        settings = config.Config()

    # select language
    if settings.language is None:
        lang = gettext
    else:
        lang = gettext.translation("autobrightness", pkg_resources.resource_filename('autobrightness', 'locales'), [settings.language])
    global _
    _ = lang.gettext

    camera = webcam.Camera( settings.camera )
    display = brightness.Display(settings.backend, lang)

    if args.start:
        print(_("Starting daemon..."))

        def shortcut(e = None):
            print(_("Shortcut key used."))
            autobrightness(camera, display)

        if not settings.shortcut is None:
            if type(settings.shortcut) == str:
                keyboard.add_hotkey(settings.shortcut, shortcut)
            else:
                keyboard.on_press_key(settings.shortcut, shortcut)

        while True:
            if settings.interval > 0:
                time.sleep( settings.interval )
                autobrightness(camera, display)
            elif not settings.shortcut is None:
                time.sleep(1)
            else:
                print(_("No interval nor shortcut selected. Exiting."))
                break
    elif args.set:
        autobrightness(camera, display)
    else:
        gui.show(lang, settings)

if __name__ == "__main__":
    main()
