import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from autobrightness import config
from autobrightness.gui import trayicon, daemon, settingswindow, logwindow
import gettext


class TrayiconTest(unittest.TestCase):
    def initTrayIcon(self):
        self.app = QApplication([])
        self.trayIcon = trayicon.TrayIcon(config.Config(), daemon.Service(), self.app, gettext)
    
    def triggerMenuAction(self, actionName):
        for action in self.trayIcon.contextMenu().actions():
            if action.objectName() == actionName:
                action.trigger()

    def findWidget(self, widgetType):
        view = None
        for widget in self.app.allWidgets():
            if type(widget) == widgetType:
                view = widget
        return view

    def test_settingsaction(self):
        self.initTrayIcon()
        self.triggerMenuAction("settings")
        view = self.findWidget(settingswindow.SettingsWindow)
        self.assertIsInstance(view, settingswindow.SettingsWindow)
    
    def test_logsaction(self):
        self.initTrayIcon()
        self.triggerMenuAction("logs")
        view = self.findWidget(logwindow.LogWindow)
        self.assertIsInstance(view, logwindow.LogWindow)
