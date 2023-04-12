from flask import Flask, request, jsonify
from PIL import Image
import io
import os
from pathlib import Path
from dotenv import load_dotenv
from evaluation import evaluate


app = Flask(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


@app.route('/get-emotions', methods=['POST'])
def get_evaluation():
    image_bytes = request.files['image'].read()
    image = Image.open(io.BytesIO(image_bytes))
    image.save('test.jpeg')

    evaluation = evaluate(image)

    return jsonify(evaluation)


if __name__ == '__main__':
    load_dotenv(os.path.join(BASE_DIR, '../.env'))
    app.run(debug=os.getenv('DEBUG'), host='0.0.0.0', port=5001)