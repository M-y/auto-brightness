from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QStyle, QMenu
from PyQt5.QtCore import QTimer
from autobrightness.gui import settingswindow, settingscontroller

class TrayIcon(QSystemTrayIcon):
    def __init__(self, config, service, app, lang):
        self.lang = lang
        global _
        _ = self.lang.gettext
        QSystemTrayIcon.__init__(self)
        self.config = config
        self.service = service
        self.app = app
        self.setIcon( QApplication.style().standardIcon(QStyle.SP_DialogOkButton) )
        self.setContextMenu(QMenu())

        settingsAction = self.contextMenu().addAction(_("Settings"))
        settingsAction.triggered.connect(self.configWindow)
        quitAction = self.contextMenu().addAction(_("Quit"))
        quitAction.triggered.connect(self.quit)

    def configWindow(self):
        """
        Shows settings window
        """
        self.service.stop()
        view = settingswindow.Window(self.lang)
        view.show()
        settingscontroller.Controller(view, self.config, self.service, self.lang)

    def quit(self):
        self.service.stop()
        self.app.quit()