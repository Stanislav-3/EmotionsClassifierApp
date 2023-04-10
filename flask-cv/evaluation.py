from flask import Flask, request
from PIL import Image
import io


app = Flask(__name__)


@app.route('/get-emotions', methods=['POST'])
def evaluate():
    image_bytes = request.files['image'].read()

    image = Image.open(io.BytesIO(image_bytes))
    image.save('test.jpeg')
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)