from mrz import MrzReader
from cam import Camera
from face_detection.mtcnn_pytorch import FaceDetector
from face_recognition.facenet_pytorch import FaceEmbedder
import time
import asyncio
import multiprocessing as mp
import numpy as np
from utils import Timer, bboxes_on_image
import cv2

import sys
sys.path.append('../java-card-reader')
from java_card_reader import CardReader

class Main:
    def __init__(self, mrz_port="COM3", show=True, test_nns=True): # "/dev/ttyACM0"
        self.show = show
        self.camera = Camera()
        # self.mrz_reader_py = MrzReader(mrz_port)
        self.card_reader = CardReader()
        self.card_reader.set_mrz_port(mrz_port)
        self.face_detector = FaceDetector()
        self.face_embedder = FaceEmbedder()
        if test_nns:
            face = self.face_detector.img2face(cv2.imread('face.jpg'))
            emb = self.face_embedder.face2embedding(face)

    
    def main(self, manual_brake=None):
        timer = Timer()
        with timer.time(f'total'):
            with timer.time(f'mrz+chip'):
                chip_img_future = self.card_reader.read_image_bytes_async()
                while not chip_img_future.isDone() or manual_brake:
                    frame = self.camera.read()
                    try:
                        with timer.time(f'face_det'):
                            face = self.face_detector.img2face(frame) # [3,h,w]
                        with timer.time(f'face_emb'):
                            embedding = self.face_embedder.face2embedding(face)
                    except: # face not found
                        continue
                    if self.show:
                        face = np.array(face.permute(1,2,0))
                        frame[:face.shape[0],:face.shape[1],:] = face
                        manual_brake = self.camera.show_frame(frame)

            with timer.time(f'comparison'):
                chip_img = self.card_reader.bytes2np(chip_img_future.get())
                chip_face = self.face_detector.img2face(chip_img)
                chip_embedding = self.face_embedder.face2embedding(chip_face)
        
        timer.print_stats()



if __name__ == '__main__': Main().main()