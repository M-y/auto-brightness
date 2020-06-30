from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from autobrightness.gui import settingswindow, settingscontroller, logwindow, aboutwindow
import autobrightness
from functools import partial

class TrayIcon(QSystemTrayIcon):
    def __init__(self, config, service, app, lang):
        self.lang = lang
        global _
        _ = self.lang.gettext
        
        QSystemTrayIcon.__init__(self)
        self.config = config
        self.service = service
        self.service.start()
        self.app = app
        self.setIcon( QIcon(autobrightness.ICON) )
        self.setContextMenu(QMenu())

        settingsAction = self.contextMenu().addAction(_("Settings"))
        settingsAction.setObjectName("settings")
        settingsAction.triggered.connect(self.configWindow)

        logAction = self.contextMenu().addAction(_("Daemon logs"))
        logAction.setObjectName("logs")
        logAction.triggered.connect(self.logWindow)

        aboutAction = self.contextMenu().addAction(_("About"))
        aboutAction.setObjectName("about")
        aboutAction.triggered.connect(self.aboutWindow)

        quitAction = self.contextMenu().addAction(_("Quit"))
        quitAction.triggered.connect(self.quit)

        if not config.configFileExists():
            self.configWindow()

    def configWindow(self):
        """
        Shows settings window
        """
        self.service.stop()
        self.configWindow_view = settingswindow.SettingsWindow(self.lang)
        self.configWindow_view.setWindowModality(Qt.ApplicationModal)
        self.configWindow_view.show()
        settingscontroller.SettingsController(self.configWindow_view, self.config, self.service, self.lang)
    
    def logWindow(self):
        """
        Shows daemon logs
        """
        self.logWindow_view = logwindow.LogWindow(self.lang)
        self.logWindow_view.setWindowModality(Qt.ApplicationModal)
        self.logWindow_view.showMaximized()

        # start the timer that reads logs
        self.logWindow_view.timer = QTimer(self.logWindow_view)
        self.logWindow_view.timer.timeout.connect(self.readLog)
        self.logWindow_view.timer.start(100)
        # stop the timer on window close
        self.logWindow_view.closeEvent = partial(self.stopLogTimer)

    def readLog(self):
        """
        Read logs from stdout and write to textedit
        """
        line = self.service.stdout()
        if len(line) > 0:
            self.logWindow_view.append(line)
    
    def stopLogTimer(self, e):
        self.logWindow_view.timer.stop()

    def quit(self):
        self.service.stop()
        self.app.quit()
    
    def aboutWindow(self):
        """
        Shows about window
        """
        self.aboutWindow_view = aboutwindow.AboutWindow(self.lang)
        self.aboutWindow_view.setWindowModality(Qt.ApplicationModal)
        self.aboutWindow_view.show()
