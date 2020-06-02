from autobrightness.backend import *

class Display:
    """
    Class for getting and setting display brightness value
    
    Parameters: 
        backend (string)
    """
    maxBrightness = 100
    
    def __init__(self, backend):
        if backend == 'sysfs':
            self.backend = sysfs.sysfs()
        
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
        self.backend.setBrightness(val)