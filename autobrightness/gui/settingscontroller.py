from functools import partial
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from autobrightness import webcam, screen
from autobrightness.gui import camerawindow
import autobrightness
import keyboard
import time
import cv2
import math
import os

class SettingsController:

    def __init__(self, view, config, service, lang):
        self.lang = lang
        global _
        _ = self.lang.gettext
        self._view = view
        self._config = config
        self._service = service
        
        self.interval_modes = [
            _("disabled"),
            _("seconds"),
            _("minutes")
        ]
        # fill form
        for dirname in os.listdir( os.path.join(autobrightness.ROOT_DIR, "locales") ):
            if os.path.isdir( os.path.join(autobrightness.ROOT_DIR, "locales", dirname) ):
                self._view.languageCombo.addItem(dirname)
        self._view.languageCombo.setCurrentText(str(self._config.language))
        
        for backendName in screen.Screen.getBackends():
            self._view.backendCombo.addItem(backendName)
        self._view.backendCombo.setCurrentText(str(self._config.backend))
        self._backendComboChange()
        
        self._view.cameraEdit.setText(str(self._config.camera))
        self._view.intervalEdit.setValue(self._config.interval)
        self._intervalChange(self._config.interval)
        self._view.shortcutEdit.setText(str(self._config.shortcut))
        self._view.gainSlider.setValue(self._config.gain)
        self._gainChange(self._config.gain)
        if self._config.fullscreen == 1:
            self._view.fullscreenCheck.setChecked(True)
        if self._config.startup == 1:
            self._view.startupCheck.setChecked(True)

        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):
        self._view.backendCombo.currentIndexChanged.connect(partial(self._backendComboChange))
        self._view.saveButton.clicked.connect(partial(self._saveButtonClick))
        self._view.shortcutButton.clicked.connect(partial(self._shortcutButtonClick))
        self._view.cameraButton.clicked.connect(partial(self._cameraButtonClick))
        self._view.backendButton.clicked.connect(partial(self._backendButtonClick))
        self._view.intervalEdit.valueChanged.connect(partial(self._intervalChange))
        self._view.gainSlider.valueChanged.connect(partial(self._gainChange))
        self._view.closeEvent = partial(self.closeEvent, self._view)
    
    def closeEvent(self, window, event):
        self._service.start()
    
    def _backendComboChange(self):
        def clearlayout(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        clearlayout(item.layout())
        
        clearlayout(self._view.backendLayout)
        self._config.backend = self._view.backendCombo.currentText()
        self.backend = screen.Screen(self._config, self.lang)
        self.backend.configWindow(self._view.backendLayout)

    def _saveButtonClick(self):
        """
        Save button click event
        """
        if len(self._view.languageCombo.currentText()) > 0:
            self._config.language = self._view.languageCombo.currentText()
        self._config.backend = self._view.backendCombo.currentText()
        self._config.gain = self._view.gainSlider.value()
        self._config.camera = self._view.cameraEdit.text()
        self._config.shortcut = self._view.shortcutEdit.text()

        self._config.interval = self._view.intervalEdit.value()
        if self._view.intervalLabel.text() == self.interval_modes[2]:
            self._config.interval *= 60

        self._config.fullscreen = 0
        if self._view.fullscreenCheck.isChecked():
            self._config.fullscreen = 1
        self._config.startup = 0
        if self._view.startupCheck.isChecked():
            self._config.startup = 1

        self.backend.configSave()
        self._config.save()

        self._view.close()

    def _shortcutButtonClick(self):
        """
        Shortcut button click event
        """
        QMessageBox.information(self._view, "", _("Close this message and press a key or key combination. "))

        key = keyboard.read_hotkey(True)
        if key == 'unknown':
            QMessageBox.information(self._view, "", _("Press again."))

            key = keyboard.read_event(True)
            self._view.shortcutEdit.setText( str(key.scan_code) )
        else:
            self._view.shortcutEdit.setText( key )

    def _cameraButtonClick(self):
        """
        Camera test button click event
        """
        try:
            camLoc = int(self._view.cameraEdit.text())
        except ValueError:
            camLoc = self._view.cameraEdit.text()

        camera = webcam.Camera(camLoc)
        camera.open()
        if camera.deviceOpened():
            details = dict()
            details["backendName"] = camera.backendName()
            details["bInfo"] = camera.cv_buildInformation()
            details["properties"] = camera.properties()
            
            camera.disable_autoExposure()
            ret, frame = camera.getFrame()
            if ret:
                self.camera_view = camerawindow.CameraWindow(self.lang)

                rgb = camera.rgbColor(frame)
                hsv = camera.hsvColor(frame)
                self.camera_view.createImages(rgb, hsv)

                if camera._oldval_autoExposure != float(0) and camera._oldval_autoExposure  == camera.getProp(cv2.CAP_PROP_AUTO_EXPOSURE):
                    details["exposure_available"] = False
                else:
                    details["exposure_available"] = True

                details["brightness"] = round( 100 * camera.getBrightness() / 255 )
                self.camera_view.createDetails(details)

                self.camera_view.setWindowModality(Qt.ApplicationModal)
                self.camera_view.showMaximized()
            else:
                QMessageBox().warning(self._view, "", _("Can't get frame from camera."))
            camera.enable_autoExposure()
        else:
            QMessageBox().warning(self._view, "", _("Can't open device."))
        camera.close()

    def _backendButtonClick(self):
        """
        Backend test button click event
        """
        QMessageBox.information(self._view, "", _("Will test min and max brightness via the selected backend."))

        self.backend.configSave()
        oldBrightness = self.backend.getBrightness()
        self.backend.setBrightness(0)
        time.sleep(1)
        self.backend.setBrightness(self.backend.backend.getMaxBrightness())
        time.sleep(1)
        self.backend.setBrightness(oldBrightness)

    def _intervalChange(self, value):
        """
        Interval change event
        """
        if self._view.intervalLabel.text() == self.interval_modes[2]:
            value *= 60
        if value > 59:
            self._view.intervalEdit.setValue( math.ceil(value / 60) )

        # update label
        if value > 59:
            self._view.intervalLabel.setText(self.interval_modes[2])
        elif value > 0:
            self._view.intervalLabel.setText(self.interval_modes[1])
        else:
            self._view.intervalLabel.setText(self.interval_modes[0])

    def _gainChange(self, value):
        self._view.gainLabel.setText( _("%s%%" % self._view.gainSlider.value()) )
