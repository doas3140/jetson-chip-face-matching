from facenet_pytorch import MTCNN
import torch

class FaceDetector:
    def __init__(self):
        self.mtcnn = MTCNN(image_size=160, margin=14, post_process=False, keep_all=False)

    def img2face(self, img): # np.array<int> [h,w,3] or [h,w] w/ 0-255 range
        img = torch.tensor(img)
        if len(img.shape) == 2: # grayscale
            img = torch.cat([img.unsqueeze(0)]*3).permute(1,2,0)
        return self.mtcnn(img) # [3,h,w]