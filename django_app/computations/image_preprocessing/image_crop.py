from PIL import Image
import numpy as np


def get_cropped_images(image: Image, boxes: np.array) -> list[Image]:
    cropped_images = []

    i = 0
    for box in boxes:
        cropped = image.crop((box[0], box[1], box[0] + box[2], box[1] + box[3]))
        cropped.save(f'computations/image_preprocessing/test/cropped{i}.jpeg')
        cropped_images.append(cropped)

        i += 1

    return cropped_images


def get_resized_images(images: list[Image], new_size=(48, 48)) -> list[Image]:
    resized_images = []

    i = 0
    for image in images:
        resized = image.resize(new_size)
        resized.save(f'computations/image_preprocessing/test/resized{i}.jpeg')
        resized_images.append(resized)

        i += 1

    return resized_images
