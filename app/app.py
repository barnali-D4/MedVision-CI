
from flask import Flask, render_template, request, jsonify
from PIL import Image, UnidentifiedImageError

from app.image_validator import validate_image
from ml.predict import predict_image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("image")

    is_valid, message = validate_image(uploaded_file)

    if not is_valid:
        return jsonify({"error": message}), 400

    try:
        image = Image.open(uploaded_file.stream)
        result = predict_image(image)

        return jsonify({
            "message": "Image classified successfully.",
            "filename": uploaded_file.filename,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "disclaimer": (
                "Educational prototype only. "
                "Not intended for clinical diagnosis."
            )
        }), 200

    except (UnidentifiedImageError, OSError):
        return jsonify({
            "error": "Unable to read the uploaded image."
        }), 400


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "File size must not exceed 10 MB."
    }), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
