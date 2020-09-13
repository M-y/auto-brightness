from PyQt5.QtWidgets import  QDialog, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QFrame, QSpinBox, QLabel, QSlider, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import autobrightness

class SettingsWindow(QDialog):
    def __init__(self, lang):
        global _
        _ = lang.gettext
        super().__init__()
        
        self.setWindowTitle(_('Settings'))
        self.setWindowIcon( QIcon(autobrightness.ICON) )

        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

        layout = QVBoxLayout()
        layout.addWidget( self._language() )
        layout.addWidget( self._backend() )
        layout.addWidget( self._camera() )
        layout.addWidget( self._interval() )
        layout.addWidget( self._shortcut() )
        layout.addWidget( self._fullscreen() )
        layout.addWidget( self._startup() )
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
        form.addRow(_('Language:'), self.languageCombo)

        frame = self._frame()
        frame.setLayout(form)
        return frame
    
    def _backend(self):
        form = QFormLayout()

        self.backendCombo = QComboBox()
        form.addRow(_('Backend:'), self.backendCombo)

        self.backendLayout = QVBoxLayout()
        form.addRow(self.backendLayout)

        self.backendButton = QPushButton(_('Test Backend'))
        form.addRow(self.backendButton)

        layout = QVBoxLayout()
        self.gainSlider = QSlider(Qt.Horizontal)
        self.gainSlider.setMinimum(-50)
        self.gainSlider.setMaximum(50)
        self.gainLabel = QLabel()
        self.gainLabel.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.gainLabel)
        layout.addWidget(self.gainSlider)
        form.addRow(_("Gain"), layout)

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

        layout = QHBoxLayout()
        self.intervalEdit = QSpinBox()
        self.intervalEdit.setMaximum(60)
        self.intervalLabel = QLabel()
        layout.addWidget(self.intervalEdit)
        layout.addWidget(self.intervalLabel)

        form.addRow(_('Interval:'), layout)
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
    
    def _fullscreen(self):
        self.fullscreenCheck = QCheckBox(_("Max brightness on full screen"))
        return self.fullscreenCheck

    def _startup(self):
        self.startupCheck = QCheckBox(_("Set brightness on startup"))
        return self.startupCheck
