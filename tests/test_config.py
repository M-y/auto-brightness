import unittest
from autobrightness import config
import os

unittest.TestLoader.sortTestMethodsUsing = None
class ConfigTest(unittest.TestCase):
    configfile = os.path.dirname(os.path.abspath(__file__)) + "/test"

    def test01(self):
        if os.path.exists(self.configfile):
            os.remove(self.configfile)
    
    def test02_init(self):
        configIns = config.Config(self.configfile)
        self.assertIsInstance(configIns, config.Config)

        configIns = config.Config()
        configIns.save()
        self.assertTrue(os.path.exists(os.path.join(os.path.expanduser("~"), ".autobrightness")))
    
    def test03_saveload(self):
        configIns = config.Config(self.configfile)
        configIns.save()
        configIns.load()
        self.assertEqual(configIns.interval, 0)

    def test04_setOption(self):
        configIns = config.Config(self.configfile)
        configIns.setOption("test", "value", 1)
        configIns.setOption("test", "valuestr", "str")
        configIns.setOption("test", "None", None)
        configIns.save()
    
    def test05_getOptin(self):
        configIns = config.Config(self.configfile)
        self.assertEqual(configIns.getOption("test", "value", int), 1)
        self.assertEqual(configIns.getOption("test", "valuestr"), "str")
        self.assertEqual(configIns.getOption("test", "valuestr", int), "str")
        self.assertIsNone(configIns.getOption("test", "None"))
        self.assertIsNone(configIns.getOption("test", "notexists"))
    
    def test06(self):
        os.remove(self.configfile)
