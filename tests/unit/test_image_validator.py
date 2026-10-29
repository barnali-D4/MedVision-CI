
import io
import sys
from pathlib import Path

from werkzeug.datastructures import FileStorage

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.image_validator import validate_image


def test_valid_png():
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="white").save(buffer, format="PNG")
    buffer.seek(0)

    uploaded = FileStorage(
        stream=buffer,
        filename="test.png",
        content_type="image/png",
    )

    valid, message = validate_image(uploaded)

    assert valid is True
    assert message == "Image is valid."


def test_reject_unsupported_extension():
    uploaded = FileStorage(
        stream=io.BytesIO(b"test"),
        filename="document.pdf",
    )

    valid, message = validate_image(uploaded)

    assert valid is False
    assert "Only PNG and JPEG" in message


def test_reject_corrupt_image():
    uploaded = FileStorage(
        stream=io.BytesIO(b"this is not an image"),
        filename="fake.png",
    )

    valid, message = validate_image(uploaded)

    assert valid is False
    assert "not a valid image" in message


def test_reject_missing_file():
    valid, message = validate_image(None)

    assert valid is False
    assert message == "Please select an image."
