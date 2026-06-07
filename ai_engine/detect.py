# TRACK 1: AI Engine
# Assigned to: Jatin
# Goal: Load the trained YOLO model and run inference on an image

from ultralytics import YOLO
import cv2
import os

# Placeholder for when Jatin trains the model.
# Put your 'best.pt' file in the 'models/' directory.
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "best.pt")

def load_model():
    """Loads the YOLOv8 model. Returns None if model doesn't exist yet."""
    if not os.path.exists(MODEL_PATH):
        print(f"⚠️ Warning: Model not found at {MODEL_PATH}. Using dummy mode.")
        return None
    return YOLO(MODEL_PATH)

def run_inference(image_path):
    """
    Takes an image path, runs YOLO detection, and returns the processed image path.
    (This is the function Teammate 1 will import into the Gradio UI).
    """
    model = load_model()
    
    if model is None:
        # DUMMY MODE: Just return the original image if model isn't trained yet
        # This allows Teammate 1 to keep building the UI without waiting for Jatin!
        return image_path
        
    # Real Inference Mode
    results = model(image_path)
    
    # Save the output image with bounding boxes
    output_path = "output_detected.jpg"
    
    # Plotting results on the image and saving
    res_plotted = results[0].plot()
    cv2.imwrite(output_path, res_plotted)
    
    return output_path

if __name__ == "__main__":
    # Test your script locally here
    print("Testing inference engine...")
    # run_inference("../data/sample_images/test.jpg")
