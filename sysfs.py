import subprocess

class sysfs:
    def getMaxBrightness(self):
        file = open("/sys/class/backlight/intel_backlight/max_brightness", "r")
        maxBrightness = int( file.read() )
        file.close()
        return maxBrightness
    
    def getBrightness(self):
        file = open("/sys/class/backlight/intel_backlight/actual_brightness", "r")
        brightness = int( file.read() )
        file.close()
        return brightness
    
    def setBrightness(self, val):
        file = open("/sys/class/backlight/intel_backlight/brightness", "w")
        file.write( str(val) )
        file.close()
        
