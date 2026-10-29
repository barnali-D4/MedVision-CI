
from io import BytesIO

from PIL import Image, UnidentifiedImageError


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def validate_image(file_storage):
    """Validate an uploaded image's extension and actual image content."""

    if file_storage is None or not file_storage.filename:
        return False, "Please select an image."

    filename = file_storage.filename.lower()

    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return False, "Only PNG and JPEG images are allowed."

    try:
        image_bytes = file_storage.read()
        file_storage.stream.seek(0)

        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()

        return True, "Image is valid."

    except (UnidentifiedImageError, OSError, ValueError):
        return False, "The uploaded file is not a valid image."
