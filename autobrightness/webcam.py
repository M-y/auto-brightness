import cv2

class Camera:
    """
    Parameters:
        device (int|string): id or path of camera
    """
    def __init__(self, device):
        self.deviceId = device
        self.device = cv2.VideoCapture()
    
    def open(self):
        """
        Open device
        """
        self.device.open(self.deviceId)
    
    def close(self):
        """
        Close device
        """
        self.device.release()

    def deviceOpened(self):
        """
        Returns: bool
        """
        if self.device is None or not self.device.isOpened():
            return False
        return True

    def disable_autoExposure(self):
        """
        Need to disable auto exposure for determining the image brightness correctly

        @note Call after open()
        """
        self._oldval_autoExposure = self.getProp(cv2.CAP_PROP_AUTO_EXPOSURE)
        self._oldval_exposure = self.getProp(cv2.CAP_PROP_EXPOSURE)

        self.setProp(cv2.CAP_PROP_AUTO_EXPOSURE, float(0))
        self.setProp(cv2.CAP_PROP_EXPOSURE, float(1))
    
    def enable_autoExposure(self):
        """
        @note Call before close()
        """
        if hasattr(self, "_oldval_autoExposure"):
            self.setProp(cv2.CAP_PROP_AUTO_EXPOSURE, self._oldval_autoExposure)
            self.setProp(cv2.CAP_PROP_EXPOSURE, self._oldval_exposure)
        else:
            self.setProp(cv2.CAP_PROP_AUTO_EXPOSURE, float(1.0))

    def getFrame(self):
        """
        Capture a frame from camera

        Returns: tuple
            ret (bool): false on failure
            frame (array)
        """
        ret, frame = self.device.read()
        return ret, frame
    
    def __getBrightness(self, hsv):
        """
        Calculate brightness of the frame

        Parameters:
            param hsv (array): frame in hsv color

        Returns: int
            brightness between 0-255
        """
        mean = cv2.mean(hsv)
        brightness = mean[2]
        return brightness
    
    def getBrightness(self):
        """
        Get ambient light level from camera

        Returns: int 
            brightness between 0-255
        """
        ret, frame = self.getFrame()
        if ret:
            return self.__getBrightness( self.hsvColor(frame) )
        return 0
    
    def rgbColor(self, frame):
        """
        Change color model of the frame to RGB
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def hsvColor(self, frame):
        """
        Change color model of the frame to HSV (Hue, Saturation, Value)
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    def backendName(self):
        """
        Get backend name of capture device
        """
        return self.device.getBackendName()
    
    def cv_buildInformation(self):
        """
        Get OpenCV build information
        """
        return cv2.getBuildInformation()
    
    def properties(self):
        """
        Return device properties

        Returns: dict
        """
        props = dict()
        for attr in dir(cv2):
            if attr.startswith('CAP_PROP'):
                props[attr] = self.getProp(getattr(cv2, attr))
        return props
    
    def getProp(self, property):
        """
        Get device property

        Parameters:
            property: Property identifier
        """
        return self.device.get(property)

    def setProp(self, property, value):
        """
        Set device property

        Parameters:
            property: Property identifier
            value:
        Returns: bool
        """
        return self.device.set(property, value)

    def showImage(self, frame):
        cv2.imshow("test", frame)
