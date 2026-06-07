# 🛣️ StreetSense MVP Repository

Welcome to the StreetSense Hackathon MVP! 

> **DEADLINE: June 13th Pitch**
> **RULES:** Do NOT touch other people's folders until integration day (Day 5).

## 📁 Repository Structure

We are dividing the work into 3 isolated tracks to avoid merge conflicts:

```text
StreetSense_MVP/
├── ai_engine/          # TRACK 1 (Jatin) - YOLOv8 training and detection scripts
├── demo_ui/            # TRACK 2 (Teammate 1) - Gradio Web UI
├── dashboard/          # TRACK 3 (Teammate 2) - Folium Map Dashboard
├── data/               # Shared testing images and videos
└── requirements.txt    # Shared Python dependencies
```

## 🚀 Setup Instructions
1. Clone this repository to your local machine.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## 🛠️ Track Assignments

### Track 1: `ai_engine/` (Jatin)
Your job is to train the YOLOv8 model using Roboflow/Google Colab, export `best.pt`, place it in the `models/` folder, and complete the `detect.py` script so that it can be imported by the UI.

### Track 2: `demo_ui/` (Teammate 1)
Your job is to build the `app.py` script using Gradio. You need an interface that accepts an image upload and displays the output image. You will import Jatin's `run_inference()` function from `detect.py`.

### Track 3: `dashboard/` (Teammate 2)
Your job is to build the `map_generator.py` script using Folium. Generate 100 fake pothole coordinates (red and yellow dots) on a map of Ujjain or Jabalpur, and export it as an interactive `map.html` file for the pitch.
