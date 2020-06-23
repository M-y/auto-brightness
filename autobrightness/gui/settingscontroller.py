from functools import partial
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCloseEvent
from autobrightness import webcam, screen
import keyboard
import time

class Controller:
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
    
    def closeEvent(controller, window, event):
        controller._service.start()
    
    def _backendComboChange(self):
        def clearLayout(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        clearLayout(item.layout())
        
        clearLayout(self._view.backendLayout)
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
        ret, frame = camera.getImage()
        if ret:
            camera.showImage(frame)

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
        self.backend.setBrightness(self.backend.maxBrightness)
        time.sleep(1)
        self.backend.setBrightness(oldBrightness)
