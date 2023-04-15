from PIL import Image
import numpy as np


def get_cropped_images(image: Image, boxes: np.array) -> list[Image]:
    return [image.crop((box[0], box[1], box[0] + box[2], box[1] + box[3])) for box in boxes]


def get_resized_images(images: list[Image], new_size=(48, 48)) -> list[Image]:
    return [image.resize(new_size) for image in images]
