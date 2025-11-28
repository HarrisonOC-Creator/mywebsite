# projects/ml/dog_breed_model.py
import json
import torch
import torchvision.transforms as T
from PIL import Image
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "efficientnet_dog_breed_classifier.pth"
CLASS_NAMES_PATH = Path(__file__).resolve().parent / "class_names.json"

_model = None
_class_names = None
_device = torch.device("cpu")

# Adjust backbone to the one you trained on (EfficientNetV2-S shown as example)
def _build_model(num_classes: int):
    from torchvision.models import efficientnet_v2_s, EfficientNet_V2_S_Weights
    weights = EfficientNet_V2_S_Weights.DEFAULT
    model = efficientnet_v2_s(weights=None)  # no pretrained at inference
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
    return model

# Match your training-time transforms as closely as possible
_transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_model():
    global _model, _class_names
    if _model is not None:
        return _model, _class_names

    # Load class names
    with open(CLASS_NAMES_PATH, "r") as f:
        _class_names = json.load(f)
    num_classes = len(_class_names)

    # Build and load weights
    checkpoint = torch.load(MODEL_PATH, map_location=_device)
    model = _build_model(num_classes)

    # Common checkpoint formats:
    state = checkpoint.get("model_state_dict", checkpoint)
    model.load_state_dict(state)
    model.eval()
    _model = model.to(_device)
    return _model, _class_names

def predict_pil_image(img: Image.Image, topk: int = 3):
    model, class_names = load_model()
    tensor = _transform(img.convert("RGB")).unsqueeze(0).to(_device)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1).squeeze(0)
        top_probs, top_idxs = torch.topk(probs, k=topk)

    def clean_label(label: str) -> str:
        # Strip numeric prefix if present
        if "-" in label:
            label = label.split("-", 1)[1]
        # Replace underscores with spaces and title-case
        return label.replace("_", " ").title()

    results = [
        {"breed": clean_label(class_names[idx.item()]), "prob": float(top_probs[i].item()*100)}
        for i, idx in enumerate(top_idxs)
    ]

    return {
        "best_breed": results[0]["breed"],
        "best_prob": results[0]["prob"],
        "topk": results,
    }
