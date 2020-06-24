from PyQt5.QtWidgets import  QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
import autobrightness
import os

class SettingsWindow(QMainWindow):
    def __init__(self, lang):
        global _
        _ = lang.gettext
        super().__init__()
        
        self.setWindowTitle(_('Settings'))
        self.setWindowIcon( QIcon(autobrightness.ICON) )
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