import base64

import cv2
import numpy as np
from numpy.typing import NDArray
from keras_facenet import FaceNet


class Model:

    def __init__(self):
        self.embedder = FaceNet()

    def transform(self, img_base64):
        img = _load_image(img_base64)

        detections = self.embedder.extract(img, threshold=0.95)

        detections.sort(key=lambda x: x['box'][2]*x['box'][3])
        face = detections[-1]

        return face


def _load_image(b64_image: str):
    buffer = base64.b64decode(b64_image)
    arr = np.frombuffer(buffer, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def format_embedding(embedding: NDArray) -> str:
    embedding = embedding.astype('float16')
    return base64.b64encode(embedding.tobytes()).decode('ascii')


model = Model()
