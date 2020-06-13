import subprocess
import re
import os

class Powercfg():
    """
    This backend uses windows powercfg utility
    """

    brightnessString = '(Ekran parlaklığı)'

    def __init__(self, lang):
        global _
        _ = lang.gettext

        self.guid = self._subprocess("Power Setting GUID: (.*?) ")

    def _subprocess(self, regex):
        """
        Run powercfg in subprocess and return command output searched with regex

        Parameters:
            regex (string): Regular expression to search

        Returns:
            string: regex group 1
        """

        result = subprocess.Popen(["POWERCFG", "/Q"], stdout=subprocess.PIPE, encoding=os.device_encoding(0))
        foundBrightnessString = False

        for line in result.stdout.readlines():
            line = line.rstrip()
            
            # search for display brightness sub group
            if re.search(self.brightnessString, line):
                foundBrightnessString = True
            # search requested regex in sub group
            if foundBrightnessString:
                ret = re.search(regex, line)
                if ret:
                    return ret.group(1)

    def getMaxBrightness(self):
        return int(self._subprocess("Maximum Possible Setting: (.*?)$"), 16)

    def getBrightness(self):
        return int(self._subprocess("Current AC Power Setting Index: (.*?)$"), 16)

    def setBrightness(self, val):
        subprocess.call(["POWERCFG", "/SETACVALUEINDEX", "SCHEME_CURRENT", "SUB_VIDEO", self.guid, str(val)])
        print("/SETACVALUEINDEX SCHEME_CURRENT SUB_VIDEO " + self.guid + " " + str(val))