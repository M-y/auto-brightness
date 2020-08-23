import autobrightness.backend
import inspect
import importlib
import pkgutil

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
    
    def __init__(self, settings, lang):
        global _
        _ = lang.gettext
        
        if not settings.backend is None:
            # find backend class
            module = importlib.import_module('autobrightness.backend.' + settings.backend)
            x, backendClass = inspect.getmembers(module, self._isBackend)[0]
            # implement backend class
            self.backend = backendClass(lang, settings)
            self.maxBrightness = self.backend.getMaxBrightness()
    
    def _isBackend(self, backendClass) -> bool:
        return inspect.isclass(backendClass) and backendClass != autobrightness.backend.ibackend.IBackend and issubclass(backendClass, autobrightness.backend.ibackend.IBackend)
    
    @staticmethod
    def getBackends():
        backends = []
        for x, moduleName, isPackage in pkgutil.iter_modules(autobrightness.backend.__path__):
            if not isPackage and moduleName != 'ibackend':
                backends.append(moduleName)
        return backends
    
    def getBrightness(self):
        """
        Returns:
            int: screen brightness
        """
        if not self.backend is None:
            return self.backend.getBrightness()
        return 100
        
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
