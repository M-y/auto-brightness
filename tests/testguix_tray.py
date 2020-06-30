import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from autobrightness import config
from autobrightness.gui import trayicon, daemon, settingswindow, logwindow, aboutwindow
import gettext

app = QApplication([])

class TrayiconTest(unittest.TestCase):
    def test_settingsaction(self):
        trayIcon = trayicon.TrayIcon(config.Config(), daemon.Service(), app, gettext)
        for action in trayIcon.contextMenu().actions():
            if action.objectName() == "settings":
                action.trigger()
        
        view = None
        for widget in app.allWidgets():
            if type(widget) == settingswindow.SettingsWindow:
                view = widget
        self.assertIsInstance(view, settingswindow.SettingsWindow)
    
    def test_logsaction(self):
        trayIcon = trayicon.TrayIcon(config.Config(), daemon.Service(), app, gettext)
        for action in trayIcon.contextMenu().actions():
            if action.objectName() == "logs":
                action.trigger()
        
        view = None
        for widget in app.allWidgets():
            if type(widget) == logwindow.LogWindow:
                view = widget
        self.assertIsInstance(view, logwindow.LogWindow)

    def test_aboutaction(self):
        trayIcon = trayicon.TrayIcon(config.Config(), daemon.Service(), app, gettext)
        for action in trayIcon.contextMenu().actions():
            if action.objectName() == "about":
                action.trigger()
        
        view = None
        for widget in app.allWidgets():
            if type(widget) == aboutwindow.AboutWindow:
                view = widget
        self.assertIsInstance(view, aboutwindow.AboutWindow)
