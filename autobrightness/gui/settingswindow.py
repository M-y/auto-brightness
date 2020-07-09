from PyQt5.QtWidgets import  QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QFrame
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

        layout = QVBoxLayout()
        layout.addWidget( self._language() )
        layout.addWidget( self._backend() )
        layout.addWidget( self._camera() )
        layout.addWidget( self._interval() )
        layout.addWidget( self._shortcut() )
        self.generalLayout.addLayout(layout)
        
        self.saveButton = QPushButton(_('Save'))
        self.generalLayout.addWidget(self.saveButton)

    def _frame(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.Box | QFrame.Sunken)
        return frame
    
    def _language(self):
        form = QFormLayout()

        self.languageCombo = QComboBox()
        for dirname in os.listdir( os.path.join(autobrightness.ROOT_DIR, "locales") ):
            if os.path.isdir( os.path.join(autobrightness.ROOT_DIR, "locales", dirname) ):
                self.languageCombo.addItem(dirname)
        form.addRow(_('Language:'), self.languageCombo)

        frame = self._frame()
        frame.setLayout(form)
        return frame
    
    def _backend(self):
        form = QFormLayout()

        self.backendCombo = QComboBox()
        for filename in os.listdir( os.path.join(autobrightness.ROOT_DIR, "backend") ):
            if filename != "__init__.py" and filename.endswith(".py"):
                self.backendCombo.addItem( os.path.splitext(filename)[0] )
        form.addRow(_('Backend:'), self.backendCombo)

        self.backendLayout = QVBoxLayout()
        form.addRow(self.backendLayout)

        self.backendButton = QPushButton(_('Test Backend'))
        form.addRow(self.backendButton)

        frame = self._frame()
        frame.setLayout(form)
        return frame
    
    def _camera(self):
        form = QFormLayout()

        layout = QHBoxLayout()
        self.cameraEdit = QLineEdit()
        self.cameraButton = QPushButton(_('Test Camera'))
        layout.addWidget(self.cameraEdit)
        layout.addWidget(self.cameraButton)
        form.addRow(_('Camera:'), layout)

        frame = self._frame()
        frame.setLayout(form)
        return frame

    def _interval(self):
        form = QFormLayout()

        self.intervalEdit = QLineEdit()
        form.addRow(_('Interval:'), self.intervalEdit)

        frame = self._frame()
        frame.setLayout(form)
        return frame

    def _shortcut(self):
        form = QFormLayout()

        layout = QHBoxLayout()
        self.shortcutEdit = QLineEdit()
        self.shortcutButton = QPushButton(_('Select Shortcut'))
        layout.addWidget(self.shortcutEdit)
        layout.addWidget(self.shortcutButton)

        form.addRow(_('Shortcut:'), layout)
        frame = self._frame()
        frame.setLayout(form)
        return frame
    