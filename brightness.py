import sysfs

class Display:
    maxBrightness = 100
    
    def __init__(self, backend):
        if backend == 'sysfs':
            self.backend = sysfs.sysfs()
        
        self.maxBrightness = self.backend.getMaxBrightness()
    
    def getBrightness(self):
        return self.backend.getBrightness()
        
    def setBrightness(self, val):
        self.backend.setBrightness(val)
