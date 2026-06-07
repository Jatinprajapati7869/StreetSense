# TRACK 3: Dashboard Map
# Assigned to: Teammate 2
# Goal: Generate an interactive heatmap for the Pitch Deck

import folium
import random
import os

def generate_dashboard():
    print("Generating City Dashboard Map...")
    
    # Center the map on Ujjain (or change to your target city)
    # Ujjain coordinates: 23.1765, 75.7885
    city_center = [23.1765, 75.7885]
    
    # Create the base map using a dark theme which looks "techy" and professional
    m = folium.Map(location=city_center, zoom_start=13, tiles='CartoDB dark_matter')
    
    # Generate 50 fake pothole coordinates around the city center
    print("Plotting simulated road defect data...")
    for _ in range(50):
        # Add slight random variations to coordinates
        lat = city_center[0] + random.uniform(-0.05, 0.05)
        lon = city_center[1] + random.uniform(-0.05, 0.05)
        
        # Random severity from 1 to 10
        severity = random.randint(1, 10)
        
        # High severity (8-10) = Red, Medium severity (4-7) = Orange
        if severity >= 8:
            color = 'red'
            radius = 8
        else:
            color = 'orange'
            radius = 5
            
        # Add marker to the map
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            popup=f"Severity: {severity}/10<br>Type: Pothole",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
        
    # Save the map to an HTML file
    output_file = os.path.join(os.path.dirname(__file__), "streetsense_dashboard.html")
    m.save(output_file)
    print(f"✅ Map generated successfully at: {output_file}")
    print("Double click the HTML file to open it in your browser!")

if __name__ == "__main__":
    generate_dashboard()
