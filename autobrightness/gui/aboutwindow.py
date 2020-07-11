from PyQt5.QtWidgets import  QDialog, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import autobrightness

class AboutWindow(QDialog):
    def __init__(self, lang):
        global _
        _ = lang.gettext
        super().__init__()
        
        self.setWindowTitle(_('About'))
        self.setWindowIcon( QIcon(autobrightness.ICON) )

        self.generalLayout = QHBoxLayout()
        self.setLayout(self.generalLayout)

        logo = QLabel()
        pixmap = QPixmap(autobrightness.ICON)
        pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio)
        logo.setPixmap(pixmap)
        self.generalLayout.addWidget(logo)
        self.generalLayout.addSpacerItem( QSpacerItem(10,0) )

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        title = QLabel("Auto Brightness")
        font = title.font()
        font.setPointSize(30)
        title.setFont(font)

        version = QLabel(autobrightness.__version__)
        version.setAlignment(Qt.AlignRight)

        link = QLabel('<a href="https://github.com/M-y/auto-brightness">https://github.com/M-y/auto-brightness</a>')
        link.setOpenExternalLinks(True)

        vbox.addWidget(title)
        vbox.addWidget(version)
        vbox.addWidget(link)

        self.generalLayout.addLayout(vbox)
