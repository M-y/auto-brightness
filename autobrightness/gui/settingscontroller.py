from functools import partial
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from autobrightness import webcam, screen
from autobrightness.gui import camerawindow
import keyboard
import time
import cv2

class SettingsController:
    def __init__(self, view, config, service, lang):
        self.lang = lang
        global _
        _ = self.lang.gettext
        self._view = view
        self._config = config
        self._service = service
        
        # fill form
        self._view.languageCombo.setCurrentText(str(self._config.language))
        self._view.backendCombo.setCurrentText(str(self._config.backend))
        self._view.cameraEdit.setText(str(self._config.camera))
        self._view.intervalEdit.setText(str(self._config.interval))
        self._view.shortcutEdit.setText(str(self._config.shortcut))
        self._backendComboChange()

        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):
        self._view.backendCombo.currentIndexChanged.connect(partial(self._backendComboChange))
        self._view.saveButton.clicked.connect(partial(self._saveButtonClick))
        self._view.shortcutButton.clicked.connect(partial(self._shortcutButtonClick))
        self._view.cameraButton.clicked.connect(partial(self._cameraButtonClick))
        self._view.backendButton.clicked.connect(partial(self._backendButtonClick))
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
        self._config.camera = self._view.cameraEdit.text()
        self._config.interval = self._view.intervalEdit.text()
        self._config.shortcut = self._view.shortcutEdit.text()

        self.backend.configSave()
        self._config.save()
        self._service.start()

        self._view.close()

    def _shortcutButtonClick(self):
        """
        Shortcut button click event
        """
        msg = QMessageBox()
        msg.setText(_("Close this message and press a key or key combination. "))
        msg.exec()

        key = keyboard.read_hotkey(True)
        if key == 'unknown':
            msg = QMessageBox()
            msg.setText(_("Press again."))
            msg.exec()

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
        camera.disable_autoExposure()
        ret, frame = camera.getFrame()
        if ret:
            rgb = camera.rgbColor(frame)
            hsv = camera.hsvColor(frame)
            backendName = camera.backendName()
            bInfo = camera.cv_buildInformation()
            properties = camera.properties()
            if camera._oldval_autoExposure  == camera.getProp(cv2.CAP_PROP_AUTO_EXPOSURE):
                exposure_available = False
            else:
                exposure_available = True

            brightness = camera.getBrightness()
            brightness = round( 100 * brightness / 255 )

            self.camera_view = camerawindow.CameraWindow(self.lang, rgb, hsv, backendName, bInfo, properties, brightness, exposure_available)
            self.camera_view.setWindowModality(Qt.ApplicationModal)
            self.camera_view.show()
        else:
            msg = QMessageBox()
            msg.setText(_("Can't get frame from camera."))
            msg.exec()
        camera.enable_autoExposure()
        camera.close()

    def _backendButtonClick(self):
        """
        Backend test button click event
        """
        msg = QMessageBox()
        msg.setText(_("Will test min and max brightness via the selected backend."))
        msg.exec()

        self.backend.configSave()
        oldBrightness = self.backend.getBrightness()
        self.backend.setBrightness(0)
        time.sleep(1)
        self.backend.setBrightness(self.backend.backend.getMaxBrightness())
        time.sleep(1)
        self.backend.setBrightness(oldBrightness)
