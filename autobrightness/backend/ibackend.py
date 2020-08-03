from autobrightness import config
import gettext
from PyQt5.QtWidgets import QLayout

class IBackend:
    """
    Backend Interface
    """

    def __init__(self, lang:gettext, settings:config.Config):
        self.settings = settings

    def getMaxBrightness(self) -> int:
        """
        Returns max brightness value
        """
        pass

    def getBrightness(self) -> int:
        """
        Returns current brightness value
        """
        pass
    
    def setBrightness(self, val:int):
        """
        Sets brightness value
        """
        pass

    def configWindow(self, layout: QLayout):
        """
        (optional)
        This method will call when user selects your backend in the settings window.
        """
        pass

    def configSave(self):
        """
        (optional)
        This method will call when user clicks save button on settings window.
        """
        pass