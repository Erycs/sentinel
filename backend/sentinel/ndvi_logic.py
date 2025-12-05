import math

ANCHORS = [
    {'lat': 48.366, 'lng': 17.548, 'type': 'green', 'strength': 1.2, 'radius': 0.015},
    {'lat': 48.375, 'lng': 17.584, 'type': 'green', 'strength': 0.9, 'radius': 0.005},
    {'lat': 48.369, 'lng': 17.575, 'type': 'green', 'strength': 0.8, 'radius': 0.006},
    {'lat': 48.390, 'lng': 17.580, 'type': 'green', 'strength': 1.0, 'radius': 0.012},
    {'lat': 48.360, 'lng': 17.590, 'type': 'green', 'strength': 0.7, 'radius': 0.010},
    {'lat': 48.377, 'lng': 17.587, 'type': 'urban', 'strength': 1.5, 'radius': 0.008},
    {'lat': 48.385, 'lng': 17.595, 'type': 'urban', 'strength': 1.0, 'radius': 0.010},
    {'lat': 48.355, 'lng': 17.585, 'type': 'urban', 'strength': 0.8, 'radius': 0.010},
]

def get_color_for_ndvi(value):
    if value < 0: return '#d73027'     # Red
    if value < 0.2: return '#fee08b'   # Yellow
    if value < 0.4: return '#d9ef8b'   # Light Green
    if value < 0.6: return '#91cf60'   # Medium Green
    return '#1a9850'                   # Dark Green

def calculate_ndvi_for_point(lat: float, lng: float):
    green_score = 0
    urban_score = 0
    base_ndvi = 0.2

    for anchor in ANCHORS:
        dist = math.sqrt((lat - anchor['lat'])**2 + (lng - anchor['lng'])**2)
        
        if dist < anchor['radius'] * 2:
            influence = 1 - (dist / (anchor['radius'] * 2))
            influence = max(0, influence)
            
            if anchor['type'] == 'green':
                green_score += influence * anchor['strength']
            else:
                urban_score += influence * anchor['strength']

    ndvi = base_ndvi + green_score - urban_score
    
    # Add noise (using sin/cos to keep it deterministic but "noisy")
    noise = (math.sin(lat * 1000) + math.cos(lng * 2000)) * 0.05
    ndvi += noise

    return max(-1, min(1, ndvi))