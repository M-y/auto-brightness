import unittest
import cv2
from autobrightness import webcam

class WebcamTest(unittest.TestCase):

    def test_image(self):
        camera = webcam.Camera(0)
        camera.open()
        ret, frame = camera.getFrame()

        if ret:
            self.assertGreater(len( camera.hsvColor(frame) ), 0)
            self.assertGreater(len( camera.rgbColor(frame) ), 0)
            camera.showImage(frame)
        else:
            self.assertIsNone(frame)
        camera.close()
    
    def test_brightness(self):
        camera = webcam.Camera(0)
        camera.open()
        brightness = camera.getBrightness()
        self.assertGreaterEqual(brightness, 0)
        self.assertLessEqual(brightness, 255)
        camera.close()
    
    def test_strings(self):
        camera = webcam.Camera(0)
        camera.open()
        if camera.deviceOpened():
            self.assertIsInstance(camera.backendName(), str)
            self.assertIsInstance(camera.cv_buildInformation(), str)
            self.assertIsInstance(camera.properties(), dict)
        camera.close()
    
    def test_property(self):
        camera = webcam.Camera(0)
        camera.open()
        if camera.deviceOpened() and "CAP_PROP_FRAME_WIDTH" in camera.properties():
            camera.setProp(cv2.CAP_PROP_FRAME_WIDTH, 320)
            camera.setProp(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            self.assertEqual(camera.getProp(cv2.CAP_PROP_FRAME_HEIGHT), 240)
            ret, frame = camera.getFrame()
            if ret:
                self.assertEqual(len(frame), 240)
        camera.close()
