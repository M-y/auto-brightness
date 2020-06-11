from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QMessageBox
from functools import partial
from autobrightness import webcam, brightness
import autobrightness
import time
import keyboard
import imp
import os

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Auto Brightness ' + autobrightness.__version__)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createForm()
        self._createButtons()
    
    def _createForm(self):
        form = QFormLayout()
        x, projectDirectory, y = imp.find_module("autobrightness")

        self.languageCombo = QComboBox()
        for dirname in os.listdir( os.path.join(projectDirectory, "locales") ):
            if os.path.isdir( os.path.join(projectDirectory, "locales", dirname) ):
                self.languageCombo.addItem(dirname)
        form.addRow(_('Language:'), self.languageCombo)

        self.backendCombo = QComboBox()
        for filename in os.listdir( os.path.join(projectDirectory, "backend") ):
            if filename != "__init__.py" and filename.endswith(".py"):
                self.backendCombo.addItem( os.path.splitext(filename)[0] )
        form.addRow(_('Backend:'), self.backendCombo)

        self.cameraEdit = QLineEdit()
        form.addRow(_('Camera:'), self.cameraEdit)

        self.intervalEdit = QLineEdit()
        form.addRow(_('Interval:'), self.intervalEdit)

        self.shortcutEdit = QLineEdit()
        form.addRow(_('Shortcut:'), self.shortcutEdit)

        self.generalLayout.addLayout(form)
    
    def _createButtons(self):
        buttons = QHBoxLayout()

        self.shortcutButton = QPushButton(_('Select Shortcut'))
        buttons.addWidget(self.shortcutButton)
        self.cameraButton = QPushButton(_('Test Camera'))
        buttons.addWidget(self.cameraButton)
        self.backendButton = QPushButton(_('Test Backend'))
        buttons.addWidget(self.backendButton)
        self.saveButton = QPushButton(_('Save'))
        buttons.addWidget(self.saveButton)

        self.generalLayout.addLayout(buttons)

class controller:
    def __init__(self, view, config):
        self._view = view
        self._config = config
        
        # fill form
        self._view.languageCombo.setCurrentText(str(self._config.language))
        self._view.backendCombo.setCurrentText(str(self._config.backend))
        self._view.cameraEdit.setText(str(self._config.camera))
        self._view.intervalEdit.setText(str(self._config.interval))
        self._view.shortcutEdit.setText(str(self._config.shortcut))

        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):
        self._view.saveButton.clicked.connect(partial(self._saveButtonClick))
        self._view.shortcutButton.clicked.connect(partial(self._shortcutButtonClick))
        self._view.cameraButton.clicked.connect(partial(self._cameraButtonClick))
        self._view.backendButton.clicked.connect(partial(self._backendButtonClick))
    
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

        self._config.save()
        print(_("Run autobrightness --start now."))
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
        except:
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

        display = brightness.Display(self._view.backendCombo.currentText(), langObj)
        oldBrightness = display.getBrightness()
        display.setBrightness(0)
        time.sleep(1)
        display.setBrightness(display.maxBrightness)
        time.sleep(1)
        display.setBrightness(oldBrightness)



def show(lang, config):
    global langObj
    langObj = lang
    global _
    _ = langObj.gettext

    app = QApplication([])
    view = window()
    view.show()
    controller(view, config)
    app.exec_()