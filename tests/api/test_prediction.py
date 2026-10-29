
from io import BytesIO

from PIL import Image
from app.app import app


def create_test_png():
    """Create a small synthetic image for API testing."""
    buffer = BytesIO()
    Image.new("RGB", (64, 64), color="white").save(
        buffer, format="PNG"
    )
    buffer.seek(0)
    return buffer


def test_upload_returns_prediction_fields():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/upload",
            data={
                "image": (create_test_png(), "test_xray.png")
            },
            content_type="multipart/form-data",
        )

    assert response.status_code == 200

    result = response.get_json()

    assert result["prediction"] in ["NORMAL", "PNEUMONIA"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert "NORMAL" in result["probabilities"]
    assert "PNEUMONIA" in result["probabilities"]
    assert "disclaimer" in result


def test_upload_without_image_returns_error():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post("/upload", data={})

    assert response.status_code == 400
    assert "error" in response.get_json()
