from autobrightness.backend.ibackend import IBackend
import os
import sys
from PyQt5.QtWidgets import QComboBox, QFormLayout

class Sysfs(IBackend):
    """
    This backend uses /sys/class/backlight directory in sysfs.
    https://www.kernel.org/doc/Documentation/ABI/stable/sysfs-class-backlight
    """

    sysfs_dir = "/sys/class/backlight"

    def __init__(self, lang, settings):
        super().__init__(lang, settings)

        global _
        _ = lang.gettext
        self.interface = self.settings.getOption("sysfs", "interface")
        if self.interface is None:
            self.interface = '.'
        
        if not os.access(os.path.join(self.sysfs_dir, self.interface, "brightness"), os.W_OK):
            print(self.sysfs_dir + _(" is not writable!"))

    def getMaxBrightness(self):
        try:
            file = open(os.path.join(self.sysfs_dir, self.interface, "max_brightness"), "r")
        except OSError as identifier:
            print(identifier)
            return 100
        else:
            maxBrightness = int( file.read() )
            file.close()
            return maxBrightness
    
    def getBrightness(self):
        try:
            file = open(os.path.join(self.sysfs_dir, self.interface, "actual_brightness"), "r")
        except OSError as identifier:
            print(identifier)
            return 0
        else:
            brightness = int( file.read() )
            file.close()
            return brightness
    
    def setBrightness(self, val):
        try:
            file = open(os.path.join(self.sysfs_dir, self.interface, "brightness"), "w")
        except OSError as identifier:
            print(identifier)
        else:
            file.write( str(val) )
            file.close()
    
    def interfaces(self):
        """
        Get interfaces from sysfs_dir

        Returns: array
        """
        interfaces = []
        for (x, dirnames, y) in os.walk(self.sysfs_dir):
            if len(dirnames) > 0:
                for dirname in dirnames:
                    interfaces.append(dirname)
        return interfaces
    
    def configWindow(self, layout):
        interfaces = self.interfaces()
        form = QFormLayout()
        self.interfaceCombo = QComboBox()

        currentIndex = 0
        for interface in interfaces:
            self.interfaceCombo.addItem(interface)
            if self.interface == interface:
                currentIndex = self.interfaceCombo.count() - 1

        self.interfaceCombo.setCurrentIndex(currentIndex)

        form.addRow(_('Interface:'), self.interfaceCombo)
        layout.addLayout(form)
    
    def configSave(self):
        self.interface = self.interfaceCombo.currentText()
        self.settings.setOption("sysfs", "interface", self.interface)
