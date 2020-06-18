import unittest
from autobrightness import brightness, config
import gettext

class BrightnessTest(unittest.TestCase):
    def test_calculate(self):
        brightnessIns = brightness.Brightness(config.Config(), gettext)
        self.assertGreater(brightnessIns.calculate(), 0)

    def test_set(self):
        brightnessIns = brightness.Brightness(config.Config(), gettext)
        brightnessIns.set(brightnessIns.calculate())
