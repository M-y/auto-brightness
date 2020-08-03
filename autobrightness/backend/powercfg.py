from autobrightness.backend.ibackend import IBackend
import subprocess
import re
import os
from PyQt5.QtWidgets import QComboBox, QFormLayout
from autobrightness import subprocess_args

class Powercfg(IBackend):
    """
    This backend uses windows powercfg utility
    """

    def __init__(self, lang, settings):
        super().__init__(lang, settings)
        
        global _
        _ = lang.gettext
        self.guid = self.settings.getOption("powercfg", "guid")
        
        if os.name == "nt":
            self.args = subprocess_args.get_args()
            self.args.update({
                'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE
            })
        else:
            print(_("powercfg is only for Windows!"))

    def _subprocess(self, regex):
        """
        Run powercfg in subprocess and return command output searched with regex

        Parameters:
            regex (string): Regular expression to search

        Returns:
            string: regex group 1
        """

        if self.guid is None:
            return None
        result = subprocess.check_output(["POWERCFG", "/Q"], **self.args)
        foundguid = False
        
        for line in result.split("\n"):
            line = line.rstrip()
            
            # search for display brightness sub group
            if re.search(self.guid, line):
                foundguid = True
            # search requested regex in sub group
            if foundguid:
                ret = re.search(regex, line)
                if ret:
                    return ret.group(1)
    
    def _isAC(self):
        """
        Is computer plugged to AC power?
        """
        result = subprocess.check_output(["wmic", "path", "Win32_Battery", "Get", "BatteryStatus"], **self.args)
        for line in result.split("\n"):
            line = line.rstrip()
            try:
                if int(line) == 2:
                    return True
            except Exception:
                pass
        return False

    def getMaxBrightness(self):
        maxBrightness = self._subprocess("Maximum Possible Setting: (.*?)$")
        if maxBrightness is None:
            return 100
        return int(maxBrightness, 16)

    def getBrightness(self):
        if self._isAC():
            return int(self._subprocess("Current AC Power Setting Index: (.*?)$"), 16)
        return int(self._subprocess("Current DC Power Setting Index: (.*?)$"), 16)

    def setBrightness(self, val):
        if self._isAC():
            subprocess.call(["POWERCFG", "/SETACVALUEINDEX", "SCHEME_CURRENT", "SUB_VIDEO", self.guid, str(val)])
        else:
            subprocess.call(["POWERCFG", "/SETDCVALUEINDEX", "SCHEME_CURRENT", "SUB_VIDEO", self.guid, str(val)])
        subprocess.call(["POWERCFG", "/S", "SCHEME_CURRENT"])
    
    def configWindow(self, layout):
        if hasattr(self, "args"):
            form = QFormLayout()
            self.guidCombo = QComboBox()

            result = subprocess.check_output(["POWERCFG", "/Q"], **self.args)
            currentIndex = 0
            for line in result.split("\n"):
                line = line.rstrip()

                # search for GUIDs and add them to combo box
                if re.search("Power Setting GUID:", line):
                    self.guidCombo.addItem(line)
                    # select item if a GUID is available from settings
                    if not self.guid is None and re.search(self.guid, line):
                        currentIndex = self.guidCombo.count() - 1

            self.guidCombo.setCurrentIndex(currentIndex)

            form.addRow(_('Display Brightness GUID:'), self.guidCombo)
            layout.addLayout(form)
    
    def configSave(self):
        if hasattr(self, "args"):
            # get GUID from combo box selected item
            guid = re.search("Power Setting GUID: (.*?) ", self.guidCombo.currentText())
            guid = guid.group(1)
            self.guid = guid
            self.settings.setOption("powercfg", "guid", guid)
