"""
StreetSense AI Engine — Road Damage Detection
Uses YOLOv8n trained on RDD2022 dataset.
Classes: D00 (Longitudinal Crack), D10 (Transverse Crack),
         D20 (Alligator Crack), D40 (Pothole)
"""

from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os
import time

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "best.pt")

# Human-readable class names for the demo
CLASS_LABELS = {
    "D00": "Longitudinal Crack",
    "D10": "Transverse Crack",
    "D20": "Alligator Crack",
    "D40": "Pothole"
}

# Severity mapping: higher confidence + more dangerous class = higher severity
SEVERITY_WEIGHTS = {
    "D00": 0.6,   # Cracks are lower severity
    "D10": 0.6,
    "D20": 0.8,   # Alligator cracking is serious
    "D40": 1.0    # Potholes are most dangerous
}

# Cache the model so it loads once, not on every image
_model_cache = None

def get_model():
    """Load model once, cache it. Never reload during the demo."""
    global _model_cache
    if _model_cache is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Train the model first (see Stage 3 of the playbook)."
            )
        _model_cache = YOLO(MODEL_PATH)
        print(f"✅ Model loaded from {MODEL_PATH}")
    return _model_cache

def calculate_severity(class_name, confidence):
    """
    Severity = class_weight * confidence * 10, capped at 10.
    This gives judges a number they can understand.
    """
    weight = SEVERITY_WEIGHTS.get(class_name, 0.7)
    severity = round(weight * confidence * 10, 1)
    return min(severity, 10.0)

def run_inference(image_path, conf_threshold=0.25):
    """
    Main inference function. Takes an image path, returns:
    - output_image_path: path to annotated image
    - summary: dict with detection count, max severity, etc.
    """
    model = get_model()
    start_time = time.time()

    # Run detection
    results = model(image_path, conf=conf_threshold, verbose=False)
    inference_time = time.time() - start_time

    result = results[0]
    boxes = result.boxes

    # Build detection summary
    detections = []
    for box in boxes:
        cls_id = int(box.cls[0])
        cls_name = result.names[cls_id]
        conf = float(box.conf[0])
        label = CLASS_LABELS.get(cls_name, cls_name)
        severity = calculate_severity(cls_name, conf)
        detections.append({
            "class": cls_name,
            "label": label,
            "confidence": round(conf, 3),
            "severity": severity
        })

    # Sort by severity (worst first)
    detections.sort(key=lambda d: d["severity"], reverse=True)

    # Save annotated image
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "detected_output.jpg")

    # Use YOLO's built-in plot (draws boxes with labels)
    annotated = result.plot(
        conf=True,
        line_width=2,
        font_size=12
    )

    # Convert BGR (OpenCV) to RGB (PIL) and save
    img = Image.fromarray(annotated[..., ::-1])
    img.save(output_path, quality=95)

    summary = {
        "total_detections": len(detections),
        "detections": detections,
        "max_severity": max((d["severity"] for d in detections), default=0),
        "inference_time_ms": round(inference_time * 1000, 1)
    }

    return output_path, summary


def run_inference_simple(image_path):
    """
    Simplified version for Gradio — returns just the output image path.
    Gradio needs a single return value for the output Image component.
    """
    output_path, summary = run_inference(image_path)
    return output_path


if __name__ == "__main__":
    import sys
    import glob

    # Find any test images
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sample_images")
    test_images = glob.glob(os.path.join(sample_dir, "*.jpg")) + \
                  glob.glob(os.path.join(sample_dir, "*.jpeg")) + \
                  glob.glob(os.path.join(sample_dir, "*.png"))

    if not test_images:
        print("No test images found in data/sample_images/")
        print("Add some .jpg images there and re-run.")
        sys.exit(1)

    for img_path in test_images:
        print(f"\nProcessing: {img_path}")
        try:
            output_path, summary = run_inference(img_path)
            print(f"  Output saved to: {output_path}")
            print(f"  Detections: {summary['total_detections']}")
            print(f"  Max severity: {summary['max_severity']}/10")
            print(f"  Inference time: {summary['inference_time_ms']}ms")
            for d in summary["detections"]:
                print(f"    → {d['label']}: severity {d['severity']}/10 (conf: {d['confidence']})")
        except Exception as e:
            print(f"  ERROR: {e}")
