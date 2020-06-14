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
        
        self.cp = self._getcodepage()
        self.guid = self._subprocess("Power Setting GUID: (.*?) ")

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
        result = subprocess.check_output(["POWERCFG", "/Q"], **self._subprocess_args(self.cp))
        foundBrightnessString = False
        
        for line in result.split("\n"):
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
        subprocess.call(["POWERCFG", "/S", "SCHEME_CURRENT"])