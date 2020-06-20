from autobrightness import webcam, brightness, config, gui, screen, daemon
import autobrightness
import gettext
import os
import argparse

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
        daemonIns = daemon.Daemon(settings, lang)
        daemonIns.start()
    elif args.set:
        brightnessIns = brightness.Brightness(settings, lang)
        brightnessIns.set( brightnessIns.calculate() )
    else:
        gui.exec(settings, lang)

if __name__ == "__main__":
    main()
