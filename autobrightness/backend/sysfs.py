import os
import sys

class sysfs:
    """
    This backend uses /sys/class/backlight directory in sysfs.
    https://www.kernel.org/doc/Documentation/ABI/stable/sysfs-class-backlight
    """

    sysfs_dir = "/sys/class/backlight"

    def __init__(self, lang):
        global _
        _ = lang.gettext
        
        # find directory for backlight
        for (dirpath, dirname, file) in os.walk("/sys/class/backlight"):
            self.sysfs_dir = os.path.join(dirpath, dirname[0])
        
        if not os.access(os.path.join(self.sysfs_dir, "brightness"), os.W_OK):
            print(self.sysfs_dir + _(" is not writable!"))

    def getMaxBrightness(self):
        try:
            file = open(os.path.join(self.sysfs_dir, "max_brightness"), "r")
        except OSError as identifier:
            print(identifier)
        else:
            maxBrightness = int( file.read() )
            file.close()
            return maxBrightness
    
    def getBrightness(self):
        try:
            file = open(os.path.join(self.sysfs_dir, "actual_brightness"), "r")
        except OSError as identifier:
            print(identifier)
        else:
            brightness = int( file.read() )
            file.close()
            return brightness
    
    def setBrightness(self, val):
        try:
            file = open(os.path.join(self.sysfs_dir, "brightness"), "w")
        except OSError as identifier:
            print(identifier)
        else:
            file.write( str(val) )
            file.close()
        
