import cv2
from cam import Camera
from utils import Timer
from pbcvt import MTCNN

timer = Timer()

class Main:
    def __init__(self):
        self.camera = Camera()
        with timer.time(f'load'):
            self.mtcnn = MTCNN()
            self.mtcnn.init(480,640)

    def main(self, manual_brake=None):
        while not manual_brake:
            frame = self.camera.read()
            try:
                with timer.time(f'inference'):
                    bboxes = self.mtcnn.findFace(frame) # [3,h,w]
                    for x1,y1,x2,y2 in bboxes:
                        cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)
            except Exception as e: # face not found
                print(e)
                continue
            manual_brake = self.camera.show_frame(frame)
        self.camera.clean()
        timer.print_stats()


if __name__ == '__main__': Main().main()