from autobrightness import brightness
import keyboard
import time

class Daemon:
    """
    Background service

    Parameters: 
        settings: config object
        lang: gettext object
    """
    def __init__(self, settings, lang):
        global _
        _ = lang.gettext
        print(_("Starting daemon..."))
        self.brightness = brightness.Brightness(settings, lang)
        self.interval = settings.interval
        self.shortcut = settings.shortcut
    
    def shortcutEvent(self, e = None):
        """
        Shortcut keypress event
        """
        print(_("Shortcut key used."))
        self.setBrightness()
        
    def addSchortcut(self, shortcut):
        """
        Add shortcut to keyboard event

        Parameters:
            shortcut (str|int): key combination or scancode
        """
        if type(shortcut) == str:
            keyboard.add_hotkey(shortcut, self.shortcutEvent)
        else:
            keyboard.on_press_key(shortcut, self.shortcutEvent)

    def setBrightness(self):
        """
        Calculate and set screen brightness
        """
        self.brightness.set( self.brightness.calculate() )

    def start(self):
        """
        Start the daemon
        """
        if not self.shortcut is None:
            self.addSchortcut(self.shortcut)
        
        while True:
            if self.interval > 0:
                time.sleep( self.interval )
                self.setBrightness()
            elif not self.shortcut is None:
                time.sleep(1)
            else:
                print(_("No interval nor shortcut selected. Exiting."))
                break
