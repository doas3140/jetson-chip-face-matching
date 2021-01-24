from facenet_pytorch import MTCNN, InceptionResnetV1

def fixed_image_standardization(img):
    return (img - 127.5) / 128.0

class FaceEmbedder:
    def __init__(self):
        self.backbone = InceptionResnetV1(pretrained='vggface2').eval()

    def faces2embeddings(self, faces): # torch.tensor<int> [b,3,h,w]
        faces = fixed_image_standardization(faces)
        return self.backbone(faces) # [b,512]

    def face2embedding(self, face): # torch.tensor<int> [3,h,w]
        return self.faces2embeddings(face.unsqueeze(0)).squeeze() # [512]