import subprocess
import re
import os
from PyQt5.QtWidgets import QComboBox, QFormLayout

class Powercfg():
    """
    This backend uses windows powercfg utility
    """

    def __init__(self, lang, settings):
        global _
        _ = lang.gettext
        
        self.settings = settings
        self.guid = settings.getOption("powercfg", "guid")
        self.cp = self._getcodepage()

    def _subprocess_args(self, encoding = None):
        """
        Builds and returns extra arguments for subprocess
        """

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        args = {    
            'stdin': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'startupinfo': si,
            'shell':True,
            'env': os.environ
        }

        if not encoding is None:
            args.update({'encoding':encoding})

        return args

    def _getcodepage(self):
        """
        Returns active code page
        """

        cp = subprocess.check_output("chcp", **self._subprocess_args())
        cp = re.search("Active code page: (.*?)$", cp.decode())
        cp = cp.group(1)

        return "cp" + cp

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
        result = subprocess.check_output(["POWERCFG", "/Q"], **self._subprocess_args(self.cp))
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

    def getMaxBrightness(self):
        maxBrightness = self._subprocess("Maximum Possible Setting: (.*?)$")
        if maxBrightness is None:
            return 100
        return int(maxBrightness, 16)

    def getBrightness(self):
        return int(self._subprocess("Current AC Power Setting Index: (.*?)$"), 16)

    def setBrightness(self, val):
        subprocess.call(["POWERCFG", "/SETACVALUEINDEX", "SCHEME_CURRENT", "SUB_VIDEO", self.guid, str(val)])
        subprocess.call(["POWERCFG", "/S", "SCHEME_CURRENT"])
    
    def configWindow(self, layout):
        form = QFormLayout()
        self.guidCombo = QComboBox()

        result = subprocess.check_output(["POWERCFG", "/Q"], **self._subprocess_args(self.cp))
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
        # get GUID from combo box selected item
        guid = re.search("Power Setting GUID: (.*?) ", self.guidCombo.currentText())
        guid = guid.group(1)
        self.guid = guid
        self.settings.setOption("powercfg", "guid", guid)