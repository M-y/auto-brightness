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
        self.screen = screen.Screen(settings.backend, lang, settings)
    
    def calculate(self):
        """
        Calculate brightness value

        Returns: int
        """
        ambient_brightness = self.camera.getBrightness()
        calculated = round( self.screen.maxBrightness * ambient_brightness / 255 )
        
        # do not go under 1%
        if calculated * 100 / self.screen.maxBrightness < 1:
            calculated = round(self.screen.maxBrightness / 100)
        
        return calculated
    
    def set(self, value):
        """
        Set screen brightness

        Parameters:
            value (int): brightness value
        """
        print(_("Adjusting brightness to %(percentage)d%% (%(value)d)") % {'percentage': (value * 100 / self.screen.maxBrightness), 'value': value})
        self.screen.setBrightness(value)
