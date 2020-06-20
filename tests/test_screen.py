import unittest
from autobrightness import screen, config
import gettext

class ScreenTest(unittest.TestCase):
    def test_none(self):
        settings = config.Config()
        settings.backend = None
        screenIns = screen.Screen(settings, gettext)
        currentBrightness = screenIns.getBrightness()
        self.assertGreaterEqual(currentBrightness, 0)
        screenIns.setBrightness(0)
        screenIns.setBrightness(currentBrightness)
        screenIns.configSave()
