from autobrightness.backend import sysfs, powercfg

class Screen:
    """
    Class for getting and setting display brightness value
    
    Parameters: 
        backend (string)
        lang: gettext object
        settings: config object
    """

    backend = None
    maxBrightness = 100
    
    def __init__(self, backend, lang, settings):
        global _
        _ = lang.gettext
        
        if backend == 'sysfs':
            self.backend = sysfs.sysfs(lang)
        if backend == 'powercfg':
            self.backend = powercfg.Powercfg(lang, settings)
        
        if not self.backend is None:
            self.maxBrightness = self.backend.getMaxBrightness()
    
    def getBrightness(self):
        """
        Returns:
            int: screen brightness
        """
        return self.backend.getBrightness()
        
    def setBrightness(self, val):
        """
        Parameters:
            val (int): brightness value
        """
        if not self.backend is None:
            self.backend.setBrightness(val)
    
    def configWindow(self, layout):
        """
        Calls draw config window method from backend if available

        Parameters:
            layout: a QVBoxLayout object
        """
        if "configWindow" in dir(self.backend):
            self.backend.configWindow(layout)
    
    def configSave(self):
        """
        Calls configSave method from backend if available
        """
        if "configSave" in dir(self.backend):
            self.backend.configSave()
