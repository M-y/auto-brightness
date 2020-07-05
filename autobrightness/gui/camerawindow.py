from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class CameraWindow(QMainWindow):
    def __init__(self, lang, rgb, hsv, backendName, bInfo, properties, brightness, exposure_available):
        global _
        _ = lang.gettext
        super().__init__()

        self.setWindowTitle(_('Camera Test'))

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        imageVbox = QVBoxLayout()
        imageVbox.addWidget( self.frame_tolabel(rgb) )
        imageVbox.addWidget( self.frame_tolabel(hsv) )
        self.generalLayout.addLayout(imageVbox)

        propText = ""
        for i in properties:
            propText += i + " = " + str(properties[i]) + "<br>"

        details = QTextEdit()
        details.setReadOnly(True)
        details.setText(
            "<h2>" + _("Image Brightness") + "</h2>" + _("%s%%" % brightness)
            + "<h2>" + _("Backend") + "</h2>" + backendName
            + "<h2>" + _("Disable Auto Exposure") + "</h2>" + (_("supported") if exposure_available else _("not supported"))
            + "<h2>" + _("Properties") + "</h2>" + propText
            + "<h2>" + _("OpenCV Build Information") + "</h2>" + bInfo.replace("\n", "<br>")
        )

        self.generalLayout.addWidget(details)
    
    def frame_tolabel(self, frame):
        """
        Converts given frame to QLabel widget
        """
        h, w, ch = frame.shape
        image = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        photo = QLabel()
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(320, 240, Qt.KeepAspectRatio)
        photo.setPixmap(pixmap)
        return photo
