from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QMessageBox
from functools import partial
from autobrightness import webcam, brightness
import autobrightness
import time
import keyboard
import imp
import os

class Window(QMainWindow):
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

        self.languageCombo = QComboBox()
        for dirname in os.listdir( os.path.join(autobrightness.ROOT_DIR, "locales") ):
            if os.path.isdir( os.path.join(autobrightness.ROOT_DIR, "locales", dirname) ):
                self.languageCombo.addItem(dirname)
        form.addRow(_('Language:'), self.languageCombo)

        self.backendCombo = QComboBox()
        for filename in os.listdir( os.path.join(autobrightness.ROOT_DIR, "backend") ):
            if filename != "__init__.py" and filename.endswith(".py"):
                self.backendCombo.addItem( os.path.splitext(filename)[0] )
        form.addRow(_('Backend:'), self.backendCombo)

        self.backendLayout = QVBoxLayout()
        form.addRow(self.backendLayout)

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

class Controller:
    def __init__(self, view, config):
        self._view = view
        self._config = config
        
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
        self.backend = brightness.Display(self._view.backendCombo.currentText(), langObj, self._config)
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
        
        msg = QMessageBox()
        msg.setText(_("Run autobrightness --start now."))
        msg.exec()
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



def show(lang, config):
    global langObj
    langObj = lang
    global _
    _ = langObj.gettext

    app = QApplication([])
    view = Window()
    view.show()
    Controller(view, config)
    app.exec_()