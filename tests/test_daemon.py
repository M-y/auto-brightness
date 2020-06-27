import unittest
from unittest.mock import patch
from autobrightness import daemon, config
import gettext

class DaemonTest(unittest.TestCase):
    @patch("time.sleep", side_effect=InterruptedError)
    def test_defaultConfig(self, x):
        settings = config.Config()
        daemonIns = daemon.Daemon(settings, gettext)
        daemonIns.start()
    
    @patch("time.sleep", side_effect=InterruptedError)
    def test_interval(self, x):
        settings = config.Config()
        settings.interval = 1
        daemonIns = daemon.Daemon(settings, gettext)
        with self.assertRaises(InterruptedError):
            daemonIns.start()
    
    @patch("time.sleep", side_effect=InterruptedError)
    def test_shortcut(self, x):
        settings = config.Config()
        settings.shortcut = "f12"
        daemonIns = daemon.Daemon(settings, gettext)
        with self.assertRaises(InterruptedError):
            daemonIns.start()
    
    @patch("time.sleep", side_effect=InterruptedError)
    def test_interval_shortcut(self, x):
        settings = config.Config()
        settings.interval = 1
        settings.shortcut = 88
        daemonIns = daemon.Daemon(settings, gettext)
        with self.assertRaises(InterruptedError):
            daemonIns.start()
