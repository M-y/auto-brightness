from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QIcon
import autobrightness

class LogWindow(QTextEdit):
    def __init__(self, lang):
        global _
        _ = lang.gettext
        super().__init__()
        
        self.setWindowTitle(_("Daemon Logs"))
        self.setWindowIcon( QIcon(autobrightness.ICON) )
