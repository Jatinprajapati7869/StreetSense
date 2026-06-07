# TRACK 2: Demo UI
# Assigned to: Teammate 1
# Goal: Build a Gradio web interface for the live pitch demo

import gradio as gr
import sys
import os

# Add the parent directory to the path so we can import Jatin's script
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ai_engine.detect import run_inference

def process_image(input_image_filepath):
    """
    This function is called when the user clicks 'Submit' in the UI.
    It passes the uploaded image to Jatin's AI script.
    """
    print(f"Processing image: {input_image_filepath}")
    
    # Call the AI engine
    output_image_path = run_inference(input_image_filepath)
    
    return output_image_path

# Create the Gradio Interface
# Gradio automatically builds the webpage based on inputs and outputs
demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="filepath", label="Upload Dashcam/Road Photo"),
    outputs=gr.Image(type="filepath", label="StreetSense AI Output"),
    title="🛣️ StreetSense AI Demo",
    description="Upload an image of a road to detect potholes and infrastructure damage.",
    theme="default"
)

if __name__ == "__main__":
    # Start the web server on localhost
    print("Starting StreetSense Demo UI...")
    demo.launch(share=False)
