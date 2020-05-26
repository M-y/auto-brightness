import cv2

class Camera:
    def __init__(self, camera):
        self.camera = camera
    
    def getImage(self):
        cam = cv2.VideoCapture(self.camera)
        ret, frame = cam.read()
        cam.release()
        return ret, frame
    
    def __getBrightness(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mean = cv2.mean(hsv)
        brightness = mean[2]
        return brightness
    
    def getBrightness(self):
        ret, image = self.getImage()
        if ret:
            return self.__getBrightness(image)
        return 0
