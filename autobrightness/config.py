import configparser
import os

class Config:
    """
    Parameters:
        configFile (string): config file location. Will use .autobrightness in home directory if not set
    """

    configfile = configparser.ConfigParser()

    def __init__(self, configFile = None):
        if configFile is None:
            self.fileLocation = os.path.join(os.path.expanduser("~"), ".autobrightness")
        else:
            self.fileLocation = configFile

        if os.path.exists(self.fileLocation):
            self.load()
        else:
            # create default config
            if os.name == "nt":
                self.backend = "powercfg"
            else:
                self.backend = "sysfs"
            self.camera = 0
            self.interval = 0
            self.shortcut = None
            self.language = None

    def save(self):
        """
        Save config to file
        """
        # set main options
        self.setOption('autobrightness', 'backend', self.backend)
        self.setOption('autobrightness', 'camera', self.camera)
        self.setOption('autobrightness', 'interval', self.interval)
        self.setOption('autobrightness', 'shortcut', self.shortcut)
        self.setOption('autobrightness', 'language', self.language)

        with open(self.fileLocation, 'w') as IO:
            self.configfile.write(IO)
    
    def load(self):
        """
        Load config from file
        """
        self.configfile.read(self.fileLocation)

        # get main options
        self.backend = self.getOption('autobrightness', 'backend')
        self.camera = self.getOption('autobrightness', 'camera', int)
        self.interval = self.getOption('autobrightness', 'interval', int)
        self.shortcut = self.getOption('autobrightness', 'shortcut', int)
        self.language = self.getOption('autobrightness', 'language')
    
    def getOption(self, section, option, type = str):
        """
        Get an option

        Parameters:
            section (str): section name in config file
            option (str): option name
            type: option type (default: str)
        
        Returns:
            (defines with type parameter): None if not found
        """

        if not self.configfile.has_option(section, option):
            return None
        
        value = self.configfile[section][option]
        
        if value == 'None' or len(value) == 0:
            return None
        
        if type is int:
            try:
                value = self.configfile[section].getint(option)
            except ValueError:
                value = self.configfile[section].get(option)
        
        return value
    
    def setOption(self, section, option, value):
        """
        Set an option

        Parameters:
            section (str): section name in config file
            option (str): option name
            value (any): option value
        """

        if not self.configfile.has_section(section):
            self.configfile[section] = {}
        
        self.configfile[section][option] = str(value)
