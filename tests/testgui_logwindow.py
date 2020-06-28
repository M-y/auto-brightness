import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from autobrightness.gui import logwindow
import gettext

app = QApplication([])

class LogwindowTest(unittest.TestCase):
    def test_textedit(self):
        view = logwindow.LogWindow(gettext)
        view.setText("test")
        self.assertEqual(view.toPlainText(), "test")
