from paddleocr import PaddleOCR
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import numpy as np

app = Flask(__name__)
CORS(app)
ocr = PaddleOCR(use_angle_cls=True, lang="de")


@app.route("/")
def health():
    return "OK"


@app.route("/ocr", methods=["POST"])
def ocr_image():
    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    file = request.files["image"]
    img = Image.open(io.BytesIO(file.read()))
    img_array = np.array(img)
    result = ocr.ocr(img_array)  # <-- OHNE cls=True

    texts = [line[1][0] for line in result[0]]
    return jsonify({"text": " ".join(texts)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
