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

    def test_each_backend(self):
        settings = config.Config()

        for backend in screen.Screen.getBackends():
            if backend == "powercfg":
                continue

            settings.backend = backend
            screenIns = screen.Screen(settings, gettext)

            if backend == "sysfs":
                interfaces = screenIns.backend.interfaces()
                if len(interfaces) < 1:
                    continue
                settings.setOption("sysfs", "interface", interfaces[0])

            currentBrightness = screenIns.getBrightness()
            self.assertGreaterEqual(currentBrightness, 0)

            if backend == "xrandr" and currentBrightness == 0:
                continue

            screenIns.setBrightness( screenIns.maxBrightness )
            self.assertEqual(screenIns.getBrightness(), screenIns.maxBrightness)
