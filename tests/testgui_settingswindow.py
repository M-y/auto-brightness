import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from autobrightness import config
from autobrightness.gui import settingscontroller, settingswindow, daemon
import gettext
import os

app = QApplication([])

class SettingswindowTest(unittest.TestCase):
    def createWindow(self, configIns):
        service = daemon.Service()
        self.view = settingswindow.SettingsWindow(gettext)
        settingscontroller.SettingsController(self.view, configIns, service, gettext)

    def checkConfig(self, configIns):
        """
        Checks if settings on window equals config instance
        """
        self.assertEqual(self.view.languageCombo.currentText(), configIns.language)
        self.assertEqual(self.view.backendCombo.currentText(), configIns.backend)
        self.assertEqual(self.view.cameraEdit.text(), str(configIns.camera))
        self.assertEqual(self.view.intervalEdit.value(), configIns.interval)
        self.assertEqual(self.view.shortcutEdit.text(), str(configIns.shortcut))
    
    def comboChange(self, comboBox):
        """
        Loops through all items in the combo box and change to all of them
        """
        for i in range( comboBox.count() ):
            if i != comboBox.currentIndex():
                comboBox.setCurrentIndex(i)

    def pressEnter(self):
        """
        Presses enter key on QMessageBox
        """
        for widget in app.allWidgets():
            if type(widget) == QMessageBox:
                QTest.keyClick(widget, Qt.Key_Enter)

    def test_defaultConfig(self):
        self.createWindow( config.Config() )
        self.checkConfig( config.Config() )
        self.view.close()
    
    def test_saveButton(self):
        configIns = config.Config("test")
        self.createWindow(configIns)
        
        # change settings on window
        self.comboChange(self.view.languageCombo)
        self.comboChange(self.view.backendCombo)
        self.view.cameraEdit.setText("1")
        self.view.intervalEdit.setValue(1)
        self.view.shortcutEdit.setText("F12")

        # click save and check config
        QTest.mouseClick(self.view.saveButton, Qt.LeftButton)
        configIns.load()
        self.checkConfig(configIns)
        self.view.close()
        os.remove("test")

    def test_cameraButton(self):
        configIns = config.Config()
        configIns.camera = 0
        self.createWindow(configIns)
        QTimer.singleShot(1000, self.pressEnter)
        QTest.mouseClick(self.view.cameraButton, Qt.LeftButton)
        self.view.close()

        configIns.camera = "/dev/video0"
        self.createWindow(configIns)
        QTimer.singleShot(1000, self.pressEnter)
        QTest.mouseClick(self.view.cameraButton, Qt.LeftButton)
        self.view.close()
    
    def test_backend(self):
        configIns = config.Config("test")
        self.createWindow(configIns)

        for i in range( self.view.backendCombo.count() ):
            self.view.backendCombo.setCurrentIndex(i)
            QTest.mouseClick(self.view.saveButton, Qt.LeftButton)
        self.view.close()
        os.remove("test")
