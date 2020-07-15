import unittest
from autobrightness import brightness, config
import gettext

class BrightnessTest(unittest.TestCase):
    def test_calculate(self):
        settings = config.Config()
        settings.backend = None
        brightnessIns = brightness.Brightness(settings, gettext)
        self.assertGreater(brightnessIns.calculate(), 0)

        settings.gain = -100
        brightnessIns = brightness.Brightness(settings, gettext)
        self.assertGreater(brightnessIns.calculate(), 0)

        settings.gain = 100
        brightnessIns = brightness.Brightness(settings, gettext)
        self.assertLessEqual(brightnessIns.calculate(), 100)

        settings.camera = 999
        settings.gain = 0
        brightnessIns = brightness.Brightness(settings, gettext)
        self.assertGreater(brightnessIns.calculate(), 0)

    def test_set(self):
        settings = config.Config()
        settings.backend = None
        brightnessIns = brightness.Brightness(settings, gettext)
        brightnessIns.set(brightnessIns.calculate())
