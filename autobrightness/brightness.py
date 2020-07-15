from autobrightness import webcam, screen

class Brightness:
    """
    Class for calculate and set brightness
    
    Parameters: 
        settings: config object
        lang: gettext object
    """
    def __init__(self, settings, lang):
        global _
        _ = lang.gettext
        self.camera = webcam.Camera( settings.camera )
        self.screen = screen.Screen(settings, lang)
        self.gain = settings.gain
    
    def calculate(self):
        """
        Calculate brightness value

        Returns: int
        """
        self.camera.open()
        self.camera.disable_autoExposure()
        if not self.camera.deviceOpened():
            print(_("Can't open video device"))
        
        ambient_brightness = self.camera.getBrightness()
        self.camera.enable_autoExposure()
        self.camera.close()
        calculated = round( self.screen.maxBrightness * ambient_brightness / 255 )

        # apply gain
        calculated += round(self.screen.maxBrightness * self.gain / 100)
        
        # do not go under 1%
        if calculated * 100 / self.screen.maxBrightness < 1:
            calculated = round(self.screen.maxBrightness / 100)
        
        # do not go over 100%
        if calculated > self.screen.maxBrightness:
            calculated = self.screen.maxBrightness
        
        return calculated
    
    def set(self, value):
        """
        Set screen brightness

        Parameters:
            value (int): brightness value
        """
        print(_("Adjusting brightness to %(percentage)d%% (%(value)d)") % {'percentage': (value * 100 / self.screen.maxBrightness), 'value': value})
        self.screen.setBrightness(value)
