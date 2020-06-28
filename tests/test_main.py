import unittest
from autobrightness import __main__

class MainTest(unittest.TestCase):
    parser = __main__.init_argparse()

    def test_arg_set(self):
        args = self.parser.parse_args(["--set"])
        self.assertTrue(args.set)
        self.assertFalse(args.start)
        self.assertIsNone(args.config)

    def test_arg_start(self):
        args = self.parser.parse_args(["--start"])
        self.assertFalse(args.set)
        self.assertTrue(args.start)
        self.assertIsNone(args.config)

    def test_arg_set_start(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--set", "--start"])
    
    def test_arg_config_start(self):
        args = self.parser.parse_args(["--config", "test", "--start"])
        self.assertFalse(args.set)
        self.assertTrue(args.start)
        self.assertEqual(args.config, "test")

    def test_arg_config_set(self):
        args = self.parser.parse_args(["--config", "test", "--set"])
        self.assertTrue(args.set)
        self.assertFalse(args.start)
        self.assertEqual(args.config, "test")
