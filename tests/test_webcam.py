import unittest
from autobrightness import webcam

class ConfigTest(unittest.TestCase):

    def test_image(self):
        camera = webcam.Camera(0)
        ret, frame = camera.getImage()

        if ret:
            self.assertGreater(len(frame), 0)
            camera.showImage(frame)
        else:
            self.assertIsNone(frame)
    
    def test_brightness(self):
        camera = webcam.Camera(0)
        brightness = camera.getBrightness()
        self.assertGreaterEqual(brightness, 0)
