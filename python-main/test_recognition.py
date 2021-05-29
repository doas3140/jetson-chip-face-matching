import cv2
import os
import torch

from utils import Timer
from face_recognition.facenet_pytorch import FaceEmbedder

timer = Timer()

class Main:
    def __init__(self):
        with timer.time(f'load'):
            self.face_embedder = FaceEmbedder()
        

    def get_image_paths(self):
        filepaths = []
        for i,(dirpath, dirnames, filenames) in enumerate(os.walk('test_images')):
            if i > 0:
                for fn in filenames:
                    filepaths.append(os.path.join(dirpath, fn))
        return filepaths

    def name(self, filepath):
        return filepath.split('/')[1]

    def read(self, filepath):
        im = cv2.resize(cv2.imread(filepath), (160,160))
        # should extract face here (this is only test)
        im = torch.tensor(im).permute(2,1,0).to('cuda')
        return im

    def main(self):
        filepaths = self.get_image_paths()
        for fp1 in filepaths:
            for fp2 in filepaths:
                im1 = self.read(fp1)
                with timer.time(f'inference'):
                    e1 = self.face_embedder.face2embedding(im1)
                e2 = self.face_embedder.face2embedding(self.read(fp2))
                score = float((e1 - e2).norm())
                print(self.name(fp1), self.name(fp2), score, timer.D['inference'][-1])
        timer.print_stats()


if __name__ == '__main__': Main().main()