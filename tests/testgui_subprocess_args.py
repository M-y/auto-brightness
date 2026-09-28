import os
import unittest
from unittest.mock import patch

from autobrightness import subprocess_args


@unittest.skipUnless(os.name == "nt", "Windows only")
class SubprocessArgsTest(unittest.TestCase):
    @patch("autobrightness.subprocess_args.subprocess.check_output")
    def test_get_codepage_with_localized_output(self, check_output):
        check_output.return_value = b"P\xe1gina de c\xf3digo ativa: 65001\r\n"

        self.assertEqual(subprocess_args.get_codepage(), "cp65001")
