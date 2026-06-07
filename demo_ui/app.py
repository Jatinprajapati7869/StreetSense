"""
StreetSense — Live Demo Interface
Professional Gradio UI for the Hustlepreneurs Pitch
"""

import gradio as gr
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ai_engine.detect import run_inference, get_model

# Pre-load model at startup so demo doesn't lag on first image
print("⏳ Pre-loading StreetSense AI model...")
try:
    get_model()
    print("✅ Model ready. Launching UI...\n")
except FileNotFoundError as e:
    print(f"⚠️  {e}")
    print("The UI will launch but detections will fail until you add best.pt\n")

# Find sample images for the Examples section
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sample_images")
example_images = []
if os.path.exists(SAMPLE_DIR):
    for f in sorted(os.listdir(SAMPLE_DIR)):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')) and f != '.gitkeep':
            example_images.append([os.path.join(SAMPLE_DIR, f)])

def process_image(input_image):
    """Process uploaded image and return annotated output + severity report."""
    if input_image is None:
        return None, "⚠️ Please upload an image."

    try:
        output_path, summary = run_inference(input_image)
    except FileNotFoundError as e:
        return None, f"⚠️ **Model not found.** Place `best.pt` in `ai_engine/models/` and restart."
    except Exception as e:
        return None, f"⚠️ **Error during inference:** {str(e)}"

    # Build a markdown report for the text output
    report_lines = [
        f"## 🔍 Detection Report",
        f"",
        f"**Total Defects Found:** {summary['total_detections']}",
        f"**Max Severity:** {summary['max_severity']}/10",
        f"**Inference Time:** {summary['inference_time_ms']}ms",
        f"",
    ]

    if summary['total_detections'] > 0:
        report_lines.append("### Defects Detected:")
        report_lines.append("")
        report_lines.append("| # | Type | Severity | Confidence |")
        report_lines.append("|---|------|----------|------------|")
        for i, d in enumerate(summary['detections'], 1):
            sev = d['severity']
            # Color-code severity
            if sev >= 7:
                emoji = "🔴"
            elif sev >= 4:
                emoji = "🟡"
            else:
                emoji = "🟢"
            report_lines.append(
                f"| {i} | {d['label']} | {emoji} {sev}/10 | {d['confidence']:.0%} |"
            )
        report_lines.append("")

        # Overall assessment
        max_sev = summary['max_severity']
        if max_sev >= 7:
            report_lines.append("### ⚠️ Assessment: CRITICAL — Immediate repair recommended")
        elif max_sev >= 4:
            report_lines.append("### 🟡 Assessment: MODERATE — Schedule maintenance within 2 weeks")
        else:
            report_lines.append("### ✅ Assessment: LOW — Monitor during next scan cycle")
    else:
        report_lines.append("### ✅ No road damage detected. Road surface appears healthy.")

    report = "\n".join(report_lines)
    return output_path, report

# Build the Gradio interface
with gr.Blocks(
    title="StreetSense AI — Road Damage Detection",
    theme=gr.themes.Base(
        primary_hue=gr.themes.colors.blue,
        secondary_hue=gr.themes.colors.orange,
        neutral_hue=gr.themes.colors.gray,
        font=gr.themes.GoogleFont("Inter"),
    ),
    css="""
        .gradio-container { max-width: 1200px !important; }
        footer { display: none !important; }
        .gr-button-primary { background: linear-gradient(135deg, #1e3a5f, #2d6aa3) !important; }
    """
) as demo:

    gr.Markdown(
        """
        # 🛣️ StreetSense — AI Road Damage Detection

        **Upload a dashcam or road photo.** Our YOLOv8 model detects potholes, cracks, and structural
        damage, then assigns a severity score from 1-10 for municipal prioritization.

        *Trained on 26,000+ labeled road images from the international RDD2022 dataset, including Indian road conditions.*
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(
                type="filepath",
                label="📸 Upload Road Image",
                height=400
            )
            submit_btn = gr.Button(
                "🔍 Analyze Road Damage",
                variant="primary",
                size="lg"
            )
        with gr.Column(scale=1):
            output_image = gr.Image(
                type="filepath",
                label="🎯 Detection Results",
                height=400
            )

    report_output = gr.Markdown(label="📋 Severity Report")

    submit_btn.click(
        fn=process_image,
        inputs=[input_image],
        outputs=[output_image, report_output]
    )

    # Example images — judges click one and get instant results
    if example_images:
        gr.Examples(
            examples=example_images,
            inputs=[input_image],
            outputs=[output_image, report_output],
            fn=process_image,
            cache_examples=False,
            label="📂 Sample Images (click to test)"
        )

    gr.Markdown(
        """
        ---
        *StreetSense by Team Qubit — IIT Madras | Hustlepreneurs @ Paradox'26*
        """
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,           # Offline demo — no sharing needed
        show_error=True,       # Show errors in UI instead of crashing
        favicon_path=None
    )
