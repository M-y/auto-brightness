from PyQt5.QtWidgets import QDialog, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class CameraWindow(QDialog):
    def __init__(self, lang):
        global _
        _ = lang.gettext
        super().__init__()

        self.setWindowTitle(_('Camera Test'))

        self.generalLayout = QHBoxLayout()
        self.setLayout(self.generalLayout)
    
    def _frame_tolabel(self, frame):
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
    
    def createImages(self, rgb, hsv):
        """
        Create image portion of the view

        Parameters:
            rgb
            hsv
        """
        imageVbox = QVBoxLayout()
        imageVbox.addWidget( self._frame_tolabel(rgb) )
        imageVbox.addWidget( self._frame_tolabel(hsv) )
        self.generalLayout.addLayout(imageVbox)
    
    def createDetails(self, details):
        """
        Create details portion of the view

        Parameters:
            details (dict)
        """
        propText = ""
        for i in details["properties"]:
            propText += i + " = " + str(details["properties"][i]) + "<br>"

        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setLineWrapMode(QTextEdit.NoWrap)
        textEdit.setText(
            "<h2>" + _("Image Brightness") + "</h2>" + _("%s%%" % details["brightness"])
            + "<h2>" + _("Backend") + "</h2>" + details["backendName"]
            + "<h2>" + _("Disable Auto Exposure") + "</h2>" + (_("supported") if details["exposure_available"] else _("not supported"))
            + "<h2>" + _("Properties") + "</h2>" + propText
            + "<h2>" + _("OpenCV Build Information") + "</h2>" + details["bInfo"].replace("\n", "<br>")
        )

        self.generalLayout.addWidget(textEdit)
