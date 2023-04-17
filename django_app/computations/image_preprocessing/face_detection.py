import cv2
import numpy as np
from PIL import Image


def get_faces(image: Image) -> (Image, np.array):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY) if image.mode != 'L' else np.array(image)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    return faces