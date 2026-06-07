# StreetSense 🛣️

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow)

StreetSense is an edge-inference AI system designed for continuous municipal road infrastructure monitoring. By leveraging computer vision models deployed on existing city fleet vehicles (e.g., waste management trucks, public transit), StreetSense passively detects, geolocates, and severity-scores road surface anomalies such as potholes and structural degradation.

## 🏗️ Architecture Overview

The system operates on a decentralized edge-to-cloud architecture:
1. **Edge Detection Engine:** A highly optimized YOLOv8 model (TensorFlow Lite / ONNX compatible) processes video feeds at 15-30 FPS on low-power devices.
2. **Data Aggregation:** Detected anomalies are bound with geospatial data (GPS coordinates) and assigned a dynamically calculated severity score.
3. **Municipal Dashboard:** A centralized analytics platform visualizing infrastructure degradation heatmaps, enabling preemptive maintenance scheduling and automated work order generation.

## 💻 Tech Stack

- **Computer Vision:** YOLOv8 (Ultralytics), OpenCV
- **Backend & Inference:** Python 3.10+
- **Interactive UI (Demo):** Gradio
- **Geospatial Analytics:** Folium

## 📂 Repository Structure

The repository is modularized into discrete service components:

- `ai_engine/`: Core computer vision inference scripts and model weights.
- `demo_ui/`: Web-based interface for rapid prototyping and visual model evaluation.
- `dashboard/`: Geospatial mapping and heat-map analytics generation.
- `data/`: Sample inputs for regression testing and validation.

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### Environment Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/Jatinprajapati7869/StreetSense.git
   cd StreetSense
   ```

2. Initialize an isolated virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the environment:
   - **Windows:** `.venv\Scripts\activate`
   - **Unix/MacOS:** `source .venv/bin/activate`

4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage Guide

### 1. Running the Inference Engine (Standalone)
To execute the YOLOv8 model directly on a sample image payload:
```bash
python ai_engine/detect.py
```
*Note: Ensure the compiled model weights (`best.pt`) are present in the `ai_engine/models/` directory prior to execution.*

### 2. Launching the Interactive Demo UI
To initialize the web interface for visual testing and demonstration:
```bash
python demo_ui/app.py
```
The interface will be served locally. Navigate to `http://127.0.0.1:7860` in your browser.

### 3. Generating the Analytics Dashboard
To compile the simulated geospatial telemetry into an interactive heatmap:
```bash
python dashboard/map_generator.py
```
The output will be rendered as `streetsense_dashboard.html` within the dashboard directory.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
