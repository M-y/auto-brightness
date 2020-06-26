from autobrightness import webcam, brightness, config, screen, daemon
from autobrightness.gui import trayicon, daemon
import autobrightness
import gettext
import os
import sys
import argparse
from PyQt5.QtWidgets import QApplication

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

def init_argparse() -> argparse.ArgumentParser:
    """
    init command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Auto change screen brightness using webcam."
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version {autobrightness.__version__}"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--start", help="Start the daemon", action='store_true')
    group.add_argument("--set", help="Set brightness and exit", action='store_true')
    parser.add_argument("--config", help="Use alternative config file instead of .autobrightness in home directory.", type=str)

    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    
    if args.config:
        # if config argument used create file
        settings = config.Config(args.config)
        settings.save()
    else:
        settings = config.Config()

    # select language
    if settings.language is None:
        lang = gettext
    else:
        lang = gettext.translation("autobrightness", os.path.join(autobrightness.ROOT_DIR, 'locales'), [settings.language])
    global _
    _ = lang.gettext

    if args.start:
        sys.stdout = Unbuffered(sys.stdout)
        daemonIns = autobrightness.daemon.Daemon(settings, lang)
        daemonIns.start()
    elif args.set:
        brightnessIns = brightness.Brightness(settings, lang)
        brightnessIns.set( brightnessIns.calculate() )
    else:
        app = QApplication([])
        app.setApplicationName("Auto Brightness")
        app.setApplicationDisplayName("Auto Brightness")
        app.setApplicationVersion(autobrightness.__version__)
        app.setQuitOnLastWindowClosed(False)
        trayIcon = autobrightness.gui.trayicon.TrayIcon(settings, autobrightness.gui.daemon.Service(), app, lang)
        trayIcon.show()
        app.exec_()

if __name__ == "__main__":
    main()
