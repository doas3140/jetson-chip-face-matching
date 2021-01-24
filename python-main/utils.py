import pandas as pd
from collections import defaultdict
import time
import numpy as np
from tabulate import tabulate

class Timer:
    def __init__(self):
      ''' Usage:
      timer = Timer()
        with timer.time(f'random task'):
          with timer.time(f'random task2'):
            time.sleep(1)
          time.sleep(1)
      timer.show_stats()
      '''
      self.S = [] # time starts
      self.N = [] # names
      self.D = defaultdict(lambda: [])
    def time(self, name):
      self.S.append(time.time())
      self.N.append(name)
      return self
    def __enter__(self):
      pass
    def __exit__(self, exc_type, exc_val, exc_tb):
      name = self.N.pop()
      t0 = self.S.pop()
      self.D[name].append(time.time() - t0)
    def get_means_df(self):
      d = {f'{k} ({len(v)})':[np.mean(v)] for k,v in self.D.items()}
      # d.update({f'{k} (total)':[np.sum(v)] for k,v in self.D.items()})
      return pd.DataFrame(d)
    def print_stats(self):
        print(tabulate(self.get_means_df(), headers='keys', tablefmt='psql'))


import cv2
import numpy as np

# PLOT BBOXES: [N,4], where 4 = (t,l,b,r)

def bboxes_on_image(im, bboxes): # [h,w,3], [N,4]
    im = im if len(im.shape) == 3 else cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
    for bb in bboxes: # [4]
        im = cv2.rectangle(im, (bb[1],bb[0]), (bb[3],bb[2]), (255,255,0), thickness=2) 
    return im