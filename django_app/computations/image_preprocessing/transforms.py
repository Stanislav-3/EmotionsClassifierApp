from PIL import Image
import io
import base64


def image_to_bytes(image: Image, _format='JPEG') -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=_format)

    return buffer.getvalue()


def images_to_base64(images: list[Image]) -> list[str]:
    encoded_images = []

    for image in images:
        img_str = base64.b64encode(image_to_bytes(image)).decode('utf8')
        encoded_images.append(img_str)

    return encoded_images

