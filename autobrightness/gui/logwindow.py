from PyQt5.QtWidgets import QTextEdit

class LogWindow(QTextEdit):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Daemon Logs")
