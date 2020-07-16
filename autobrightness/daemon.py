from autobrightness import brightness
import keyboard
import time
import Xlib.display
from threading import Thread

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

        self.fullscreen = False
        if settings.fullscreen == 1:
            self.fullscreen = True
    
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
        if self.fullscreen:
            fullscreenThread = Thread(target=self._fullScreenCheck)
            fullscreenThread.start()

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
    
    def _fullscreenCount(self):
        """
        Returns fullscreen window count

        https://stackoverflow.com/a/1360522
        """
        screen = Xlib.display.Display().screen()

        num_of_fs = 0
        for window in screen.root.query_tree()._data['children']:
            try:
                width = window.get_geometry()._data["width"]
                height = window.get_geometry()._data["height"]
            except Exception:
                width = 0
                height = 0

            if width == screen.width_in_pixels and height == screen.height_in_pixels:
                num_of_fs += 1

        return num_of_fs

    def _fullScreenCheck(self):
        print(_("Full screen check activated."))
        fullscreenCount = self._fullscreenCount()

        oldBrightness = self.brightness.screen.getBrightness()
        while True:
            # update oldBrightness if changed while we are in the loop
            if self.brightness.screen.getBrightness() != self.brightness.screen.maxBrightness:
                oldBrightness = self.brightness.screen.getBrightness()
            
            # full screen window count increase means a full screen window is on screen
            if self._fullscreenCount() > fullscreenCount and self.brightness.screen.getBrightness() != self.brightness.screen.maxBrightness:
                print(_("Detected full screen mode"))
                self.brightness.set( self.brightness.screen.maxBrightness )
            
            # get back to old brightness value
            if self._fullscreenCount() == fullscreenCount and oldBrightness != self.brightness.screen.getBrightness():
                print(_("Exited from full screen"))
                self.brightness.set(oldBrightness)
            
            time.sleep(.5)
