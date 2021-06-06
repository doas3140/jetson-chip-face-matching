import cv2

from utils import Timer

from mrz import MrzReader

import sys
sys.path.append('../java-card-reader')
from java_card_reader import CardReader

timer = Timer()

class Main:
    def __init__(self, mrz_port="/dev/ttyACM0"):
        self.mrz_reader_py = MrzReader(mrz_port)
        self.card_reader = CardReader()
        self.card_reader.set_mrz_port(mrz_port)

    def main(self):
        mrz = self.mrz_reader_py.read_mrz()
        chip_img_future = self.card_reader.mrz2imagebytes_async(mrz)
        while not chip_img_future.isDone():
            continue
        chip_img = self.card_reader.bytes2np(chip_img_future.get())
        print('image:', chip_img.shape)



if __name__ == '__main__': Main().main()