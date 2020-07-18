import unittest
from autobrightness import screen, config
import gettext
from PyQt5.QtWidgets import QVBoxLayout, QApplication

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
    
    def test_sysfs(self):
        settings = config.Config()
        settings.backend = 'sysfs'
        settings.setOption("sysfs", "interface", "intel_backlight")
        screenIns = screen.Screen(settings, gettext)

        currentBrightness = screenIns.getBrightness()
        self.assertGreaterEqual(currentBrightness, 0)

        # screenIns.setBrightness( screenIns.maxBrightness )
        # self.assertEqual(screenIns.getBrightness(), screenIns.maxBrightness)
