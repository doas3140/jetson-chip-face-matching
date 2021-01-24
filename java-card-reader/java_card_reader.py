import time
from PIL import Image
import numpy as np
import io

from py4j.java_gateway import JavaGateway

class CardReader:
    def __init__(self):
        self.gateway = JavaGateway()
        self.card_reader = self.gateway.entry_point.getCardReader()
        self.mrz_reader = self.gateway.entry_point.getMrzReader()
        self.all_reader = self.gateway.entry_point.getMrzAndImageReader()

    def await_card(self):
        pass

    def bytes2np(self, img_bytes):
        # may need JPEG-2000 decoder (https://stackoverflow.com/questions/44782612/pillow-and-jpeg2000-decoder-jpeg2k-not-available)
        img = Image.open(io.BytesIO(img_bytes))
        img.save("im.png", "JPEG")
        return np.array(img)

    def set_mrz_port(self, port="/dev/ttyACM0", timeout=10000):
        self.mrz_reader.setPort(port, timeout)

    def get_image(self, mrz): # string -> [h,w,3] np tensor
        if self.card_reader is None:
            raise Exception('await card first!')
        img_bytes = self.card_reader.readImage(mrz)
        return self.bytes2np(img_bytes)

    def mrz2imagebytes_async(self, mrz): # returns future
        return self.card_reader.readImageAsync(mrz)

    def read_image_bytes_async(self): # returns future
        return self.all_reader.readImageBytesAsync()