from PIL import Image
import io
import base64


def images_to_base64(images: list[Image]) -> list[str]:
    encoded_images = []

    for image in images:
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf8')
        encoded_images.append(img_str)

    return encoded_images
