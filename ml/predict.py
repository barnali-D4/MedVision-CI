from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms
from torchvision.models import resnet18
from torch import nn


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "medvision_resnet18.pth"

CLASS_NAMES = {
    0: "NORMAL",
    1: "PNEUMONIA",
}

DEVICE = torch.device("cpu")

IMAGE_TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model checkpoint not found: {MODEL_PATH}"
        )

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True,
    )

    model = resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 2)

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)
    model.eval()

    return model


model = load_model()


def predict_image(image):
    """
    Classify a PIL image as NORMAL or PNEUMONIA.

    Returns the predicted class and model confidence.
    This is an educational prototype, not a clinical diagnostic tool.
    """
    if not isinstance(image, Image.Image):
        raise TypeError("Expected a PIL Image.")

    image = image.convert("RGB")
    tensor = IMAGE_TRANSFORM(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0]

    predicted_index = int(torch.argmax(probabilities).item())

    return {
        "prediction": CLASS_NAMES[predicted_index],
        "confidence": round(
            float(probabilities[predicted_index].item()), 4
        ),
        "probabilities": {
            CLASS_NAMES[i]: round(float(probabilities[i].item()), 4)
            for i in range(len(CLASS_NAMES))
        },
    }