import os
import sys

class sysfs:
    def __init__(self):
        for (dirpath, dirname, file) in os.walk("/sys/class/backlight"):
            self.sysfs_dir = os.path.join(dirpath, dirname[0])
        
        if not os.access(os.path.join(self.sysfs_dir, "brightness"), os.W_OK):
            sys.exit(self.sysfs_dir + " is not writable!")

    def getMaxBrightness(self):
        file = open(os.path.join(self.sysfs_dir, "max_brightness"), "r")
        maxBrightness = int( file.read() )
        file.close()
        return maxBrightness
    
    def getBrightness(self):
        file = open(os.path.join(self.sysfs_dir, "actual_brightness"), "r")
        brightness = int( file.read() )
        file.close()
        return brightness
    
    def setBrightness(self, val):
        file = open(os.path.join(self.sysfs_dir, "brightness"), "w")
        file.write( str(val) )
        file.close()
        
