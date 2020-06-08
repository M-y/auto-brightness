import configparser
from os import path

class Config:
    """
    Parameters:
        configFile (string): config file location. Will use .autobrightness in home directory if not set
    """
    def __init__(self, configFile = None):
        if configFile is None:
            self.fileLocation = path.join(path.expanduser("~"), ".autobrightness")
        else:
            self.fileLocation = configFile

        if path.exists(self.fileLocation):
            self.load()
        else:
            # create default config
            self.backend = None
            self.camera = 0
            self.interval = 0
            self.shortcut = None
            self.language = None

    def save(self):
        """
        Save config to file
        """
        configfile = configparser.ConfigParser()
        configfile['autobrightness'] = {}
        config = configfile['autobrightness']

        config['backend'] = str(self.backend)
        config['camera'] = str(self.camera)
        config['interval'] = str(self.interval)
        config['shortcut'] = str(self.shortcut)
        config['language'] = str(self.language)

        print(self.fileLocation)
        with open(self.fileLocation, 'w') as IO:
            configfile.write(IO)
    
    def load(self):
        """
        Load config from file
        """
        configfile = configparser.ConfigParser()
        configfile.read(self.fileLocation)
        config = configfile['autobrightness']

        if config['backend'] == 'None':
            self.backend = None
        else:
            self.backend = config['backend']

        try:
            self.camera = config.getint('camera')
        except:
            self.camera = config['camera']
        
        self.interval = config.getint('interval')

        if config['shortcut'] == 'None':
            self.shortcut = None
        else:
            try:
                self.shortcut = config.getint('shortcut')
            except:
                self.shortcut = config['shortcut']
        
        if config['language'] == 'None':
            self.language = None
        else:
            self.language = config['language']
