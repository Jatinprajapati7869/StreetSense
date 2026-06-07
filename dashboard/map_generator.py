"""
StreetSense — Municipal Dashboard Generator
Generates an interactive heatmap simulating 90 days of road damage data.
Target city: Ujjain, Madhya Pradesh (Smart City)
"""

import folium
from folium.plugins import HeatMap
import random
import os
import json

def generate_dashboard():
    print("🗺️  Generating StreetSense Municipal Dashboard...")

    # ── City Configuration ──
    # Ujjain, MP — our target Smart City
    city_name = "Ujjain"
    city_center = [23.1765, 75.7885]
    zoom_start = 13

    # ── Generate Simulated Road Damage Data ──
    # Simulate 200 detections across the city
    # Cluster them along main roads for realism (not purely random)
    random.seed(42)  # Fixed seed = same map every time = consistent demo

    # Define road corridors (approximate lat/lon of major Ujjain roads)
    road_corridors = [
        {"name": "Indore Road",      "center": [23.1850, 75.7650], "spread": 0.008},
        {"name": "Dewas Road",       "center": [23.1950, 75.7900], "spread": 0.010},
        {"name": "Agar Road",        "center": [23.1600, 75.8050], "spread": 0.007},
        {"name": "Station Road",     "center": [23.1750, 75.7800], "spread": 0.005},
        {"name": "Freeganj Area",    "center": [23.1780, 75.7750], "spread": 0.004},
        {"name": "Mahakal Temple Rd","center": [23.1828, 75.7682], "spread": 0.003},
        {"name": "Ring Road South",  "center": [23.1550, 75.7900], "spread": 0.012},
        {"name": "University Road",  "center": [23.1700, 75.8100], "spread": 0.006},
    ]

    detections = []
    detection_id = 1

    for corridor in road_corridors:
        # 20-30 detections per corridor
        n_detections = random.randint(20, 30)
        for _ in range(n_detections):
            lat = corridor["center"][0] + random.gauss(0, corridor["spread"])
            lon = corridor["center"][1] + random.gauss(0, corridor["spread"])

            # Damage type distribution: 40% potholes, 25% longitudinal, 20% transverse, 15% alligator
            damage_roll = random.random()
            if damage_roll < 0.40:
                damage_type = "Pothole"
                base_severity = random.uniform(5, 10)
            elif damage_roll < 0.65:
                damage_type = "Longitudinal Crack"
                base_severity = random.uniform(2, 7)
            elif damage_roll < 0.85:
                damage_type = "Transverse Crack"
                base_severity = random.uniform(2, 6)
            else:
                damage_type = "Alligator Crack"
                base_severity = random.uniform(6, 9)

            severity = round(base_severity, 1)

            detections.append({
                "id": f"SS-{detection_id:04d}",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "severity": severity,
                "type": damage_type,
                "corridor": corridor["name"],
                "date": f"2026-{random.randint(3,5):02d}-{random.randint(1,28):02d}",
                "vehicle": f"GarbageTruck-{random.randint(1,10):02d}"
            })
            detection_id += 1

    print(f"   Generated {len(detections)} simulated detections across {len(road_corridors)} corridors")

    # ── Create the Map ──
    m = folium.Map(
        location=city_center,
        zoom_start=zoom_start,
        tiles='CartoDB dark_matter',
        control_scale=True
    )

    # ── Add Title Overlay ──
    title_html = f"""
    <div style="
        position: fixed;
        top: 10px; left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(8px);
        padding: 12px 28px;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.4);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    ">
        <div style="color: #e0e7ff; font-size: 18px; font-weight: 700; letter-spacing: 0.5px;">
            🛣️ StreetSense — {city_name} Municipal Dashboard
        </div>
        <div style="color: #94a3b8; font-size: 12px; margin-top: 4px;">
            {len(detections)} defects detected | 10 vehicles | 90-day pilot simulation
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # ── Add Legend ──
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px; right: 20px;
        z-index: 9999;
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(8px);
        padding: 14px 18px;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #e0e7ff;
        font-size: 12px;
        line-height: 1.8;
    ">
        <div style="font-weight: 700; margin-bottom: 6px; font-size: 13px;">Severity Legend</div>
        <div><span style="color: #ef4444;">●</span> Critical (8-10) — Immediate repair</div>
        <div><span style="color: #f59e0b;">●</span> Moderate (5-7) — Schedule repair</div>
        <div><span style="color: #22c55e;">●</span> Low (1-4) — Monitor next cycle</div>
        <hr style="border-color: rgba(99,102,241,0.2); margin: 8px 0;">
        <div style="color: #94a3b8;">Data: StreetSense AI v1.0</div>
        <div style="color: #94a3b8;">Period: Mar-May 2026</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # ── Add Stats Panel ──
    critical = sum(1 for d in detections if d["severity"] >= 8)
    moderate = sum(1 for d in detections if 5 <= d["severity"] < 8)
    low = sum(1 for d in detections if d["severity"] < 5)
    potholes = sum(1 for d in detections if d["type"] == "Pothole")

    stats_html = f"""
    <div style="
        position: fixed;
        top: 80px; left: 20px;
        z-index: 9999;
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(8px);
        padding: 16px 20px;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #e0e7ff;
        font-size: 13px;
        line-height: 2;
        min-width: 200px;
    ">
        <div style="font-weight: 700; font-size: 14px; margin-bottom: 6px;">📊 Summary</div>
        <div>Total Defects: <b>{len(detections)}</b></div>
        <div><span style="color: #ef4444;">●</span> Critical: <b>{critical}</b></div>
        <div><span style="color: #f59e0b;">●</span> Moderate: <b>{moderate}</b></div>
        <div><span style="color: #22c55e;">●</span> Low: <b>{low}</b></div>
        <hr style="border-color: rgba(99,102,241,0.2); margin: 6px 0;">
        <div>Potholes: <b>{potholes}</b></div>
        <div>Vehicles: <b>10</b></div>
        <div>Days Active: <b>90</b></div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(stats_html))

    # ── Add Individual Detection Markers ──
    for d in detections:
        if d["severity"] >= 8:
            color = "#ef4444"     # red
            radius = 7
        elif d["severity"] >= 5:
            color = "#f59e0b"     # amber
            radius = 5
        else:
            color = "#22c55e"     # green
            radius = 4

        popup_html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; min-width: 180px;">
            <b style="font-size: 13px;">{d['type']}</b><br>
            <b>ID:</b> {d['id']}<br>
            <b>Severity:</b> {d['severity']}/10<br>
            <b>Corridor:</b> {d['corridor']}<br>
            <b>Detected:</b> {d['date']}<br>
            <b>Vehicle:</b> {d['vehicle']}<br>
        </div>
        """

        folium.CircleMarker(
            location=[d["lat"], d["lon"]],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=250),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=1
        ).add_to(m)

    # ── Add Heatmap Layer ──
    heat_data = [[d["lat"], d["lon"], d["severity"] / 10] for d in detections]
    HeatMap(
        heat_data,
        min_opacity=0.3,
        max_zoom=15,
        radius=20,
        blur=15,
        gradient={
            0.2: '#22c55e',
            0.5: '#f59e0b',
            0.8: '#ef4444',
            1.0: '#dc2626'
        }
    ).add_to(m)

    # ── Save ──
    output_file = os.path.join(os.path.dirname(__file__), "streetsense_dashboard.html")
    m.save(output_file)
    print(f"✅ Dashboard saved to: {output_file}")
    print(f"   → {len(detections)} detections plotted")
    print(f"   → {critical} critical, {moderate} moderate, {low} low severity")
    print(f"   Open the HTML file in Chrome for the best experience.")

    # Also save detection data as JSON (useful for pitch)
    data_file = os.path.join(os.path.dirname(__file__), "detection_data.json")
    with open(data_file, "w") as f:
        json.dump({"city": city_name, "detections": detections}, f, indent=2)
    print(f"   → Raw data saved to: {data_file}")


if __name__ == "__main__":
    generate_dashboard()
