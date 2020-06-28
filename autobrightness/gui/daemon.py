from autobrightness import subprocess_args
import subprocess
import psutil
import sys
import re

class Service():
    """
    Manages daemon as a subprocess
    """
    
    def start(self):
        args = subprocess_args.get_args()
        args.update({
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT
        })

        if not re.search("unittest", sys.argv[0]):
            autobrightness_args = ["autobrightness"]
            for i in range(1, len(sys.argv)):
                autobrightness_args.append(sys.argv[i])
            self._process = subprocess.Popen(" ".join(autobrightness_args) + " --start",  **args)
    
    def stop(self):
        if self.running():
            for child in psutil.Process(self._process.pid).children(True):
                child.terminate()
            self._process.terminate()

    def running(self):
        if hasattr(self, "_process") and self._process.poll() is None:
            return True
        return False
    
    def stdout(self):
        line = self._process.stdout.readline()
        return line.rstrip()
