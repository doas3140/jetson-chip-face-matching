from mrz import MrzReader
from cam import Camera
from face_detection.mtcnn_pytorch import FaceDetector
from face_recognition.facenet_pytorch import FaceEmbedder
from time import sleep, time
import asyncio
import multiprocessing as mp
import numpy as np
from utils import Timer, bboxes_on_image
import cv2
import sys
import torch

from utils import Timer
from pbcvt import MTCNN

import sys
sys.path.append('../java-card-reader')
from java_card_reader import CardReader

timer = Timer()

class Main:
    def __init__(self, mrz_port="/dev/ttyACM0"):
        with timer.time(f'load-total'):
            self.card_reader = CardReader()
            self.card_reader.set_mrz_port(mrz_port)
            with timer.time(f'load-mtcnn'):
                self.mtcnn = MTCNN()
                self.mtcnn.init(480,640)
            with timer.time(f'load-facenet'):
                self.face_embedder = FaceEmbedder()
            self.camera = Camera()
            #
            self.camera_face = None
            self.camera_emb = None
            self.reader_face = None
            self.reader_emb = None

    def prep_im(self, im):
        im = cv2.resize(im, (160,160))
        return torch.tensor(im).permute(2,1,0).to('cuda')

    async def camera_loop(self):
        while True:
            with timer.time(f'camera-total'):
                frame = self.camera.read()
                print('[camera] frame:', frame.shape)
                with timer.time(f'camera-mtcnn'):
                    bboxes = self.mtcnn.findFace(frame)
                print('[camera] bboxes:', bboxes)
                for x1,y1,x2,y2 in bboxes:
                    self.camera_face = frame[y1:y2,x1:x2]
                    print('[camera] face:', self.camera_face.shape)
                    with timer.time(f'camera-facenet'):
                        im = self.prep_im(self.camera_face)
                        self.camera_emb = self.face_embedder.face2embedding(im)
                await asyncio.sleep(0)

    async def reader_loop(self):
        while True:
            print('[reader] starting read...')
            chip_img_future = self.card_reader.read_image_bytes_async()
            t0 = time()
            while not chip_img_future.isDone():
                await asyncio.sleep(0)
            byte_array = chip_img_future.get()
            if len(byte_array) > 0:
                print('[reader] byte arr len:', len(byte_array))
                chip_img = self.card_reader.bytes2np(byte_array) # [h,w]
                timer.D['reader-read'].append(time() - t0)
                print('[reader] chip img:', chip_img.shape)
                chip_img = np.concatenate([chip_img[:,:,None] for _ in range(3)], axis=2) # [h,w,3]
                with timer.time(f'reader-mtcnn'):
                    bboxes = self.mtcnn.findFace(chip_img)
                print('[reader] bboxes:', bboxes)
                for y1,x1,y2,x2 in bboxes:
                    self.reader_face = chip_img[y1:y2,x1:x2]
                    print('[reader] chip face:', self.reader_face.shape)
                    with timer.time(f'reader-facenet'):
                        im = self.prep_im(self.reader_face)
                        self.reader_emb = self.face_embedder.face2embedding(im)
                    timer.D['reader-total'].append(time() - t0)
                    self.compare_embeddings_and_exit()
            
    def compare_embeddings_and_exit(self):
        if self.reader_face is None: print("[ERROR] Couldn't read face from reader...")
        if self.camera_face is None: print("[ERROR] Couldn't read face from camera...")
        cv2.imwrite('reader_face.png', self.reader_face)
        cv2.imwrite('camera_face.png', self.camera_face)
        score = float((self.reader_emb - self.camera_emb).norm())
        print('score:', score)
        timer.print_stats()
        sys.exit()

    def main(self):
        asyncio.gather(self.camera_loop(), self.reader_loop())
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__': Main().main()