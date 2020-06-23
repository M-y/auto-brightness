import subprocess
import psutil
import sys

class Service():
    """
    Manages daemon as a subprocess
    """
    
    def start(self):
        self._process = subprocess.Popen(
            " ".join(sys.argv) + " --start", 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            shell=True,
            encoding='UTF-8'
        )
    
    def stop(self):
        if self.running():
            for child in psutil.Process(self._process.pid).children(True):
                child.terminate()
            self._process.terminate()

    def running(self):
        if self._process.poll() is None:
            return True
        return False
    
    def stdout(self):
        line = self._process.stdout.readline()
        return line.rstrip()