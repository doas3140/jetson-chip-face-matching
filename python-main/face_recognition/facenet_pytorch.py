import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

def fixed_image_standardization(img):
    return (img - 127.5) / 128.0

class FaceEmbedder:
    def __init__(self, num_tries=5):
        print('loading vgg facenet...')
        self.backbone = InceptionResnetV1(pretrained='vggface2').eval().to('cuda')
        print('inferecing facenet model...')
        for i in range(num_tries):
            self.backbone(torch.randn(1,3,160,160).to('cuda'))
            print(i, '/', num_tries)
        print('facenet loaded.')

    def faces2embeddings(self, faces): # torch.tensor<int> [b,3,h,w]
        faces = fixed_image_standardization(faces)
        return self.backbone(faces) # [b,512]

    def face2embedding(self, face): # torch.tensor<int> [3,h,w]
        return self.faces2embeddings(face.unsqueeze(0)).squeeze() # [512]