from autobrightness.backend.ibackend import IBackend
import subprocess
import re

class Xrandr(IBackend):
    """
    This backend uses RandR extension by the X server
    """

    def __init__(self, lang, settings):
        super().__init__(lang, settings)
        
        global _
        _ = lang.gettext
    
    def getMaxBrightness(self):
        return 100
    
    def getBrightness(self):
        val = 0

        try:
            result = subprocess.check_output(["xrandr", "--verbose"], **{'encoding': 'UTF-8'})
        except subprocess.CalledProcessError as identifier:
            print(identifier)
            result = ""

        for line in result.split("\n"):
            line = line.rstrip()

            ret = re.search("Brightness: (.*?)$", line)
            if ret:
                val = float(ret.group(1))
        
        return int(val * 100)
    
    def setBrightness(self, val):
        val = val / 100

        for output in self._outputs():
            subprocess.call(["xrandr", "--output", output, "--brightness", str(val)])

    def _outputs(self):
        """
        Returns: list
            connected outputs
        """

        result = subprocess.check_output("xrandr", **{'encoding': 'UTF-8'})
        outputs = []
        for line in result.split("\n"):
            line = line.rstrip()

            ret = re.search("^(.*?) connected", line)
            if ret:
                outputs.append( ret.group(1) )

        return outputs
