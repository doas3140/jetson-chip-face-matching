import numpy as np
import cv2
import time

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        _, frame = self.cap.read()
        print('frame shape:', frame.shape)
        print('camera fps: {}'.format(self.cap.get(cv2.CAP_PROP_FPS)))

    def read(self): # returns np.array<int> [h,w,3]
        _, frame = self.cap.read() # [h,w,3]
        return frame

    def show_frame(self, frame):
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        return False

    def clean(self):
        self.cap.release()
        cv2.destroyAllWindows()