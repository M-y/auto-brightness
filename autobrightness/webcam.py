import cv2

class Camera:
    """
    Parameters:
        device (int|string): id or path of camera
    """
    def __init__(self, device):
        self.device = device
    
    def getImage(self):
        """
        Capture a frame from camera

        Returns: tuple
            ret (bool): false on failure
            frame (array)
        """
        cam = cv2.VideoCapture(self.device)
        ret, frame = cam.read()
        cam.release()
        return ret, frame
    
    def __getBrightness(self, image):
        """
        Change color model of the image to HSV (Hue, Saturation, Value) and calculate brightness

        Parameters:
            param image (array)

        Returns: int
            brightness between 0-255
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mean = cv2.mean(hsv)
        brightness = mean[2]
        return brightness
    
    def getBrightness(self):
        """
        Get ambient light from camera

        Returns: int 
            brightness between 0-255
        """
        ret, image = self.getImage()
        if ret:
            return self.__getBrightness(image)
        return 0
    
    def showImage(self, frame):
        cv2.imshow("test", frame)
