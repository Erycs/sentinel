from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from sentinel.ndvi_logic import calculate_ndvi_for_point, get_color_for_ndvi, calculate_regional_average_ndvi

app = FastAPI()

# Input model for the grid request
class GridRequest(BaseModel):
    north: float
    south: float
    east: float
    west: float
    resolution: int
    date_key: str # NEW: Add date key for seasonal query

# 1. API Endpoint: Calculate Grid (Modified)
@app.post("/api/ndvi-grid")
async def get_ndvi_grid(bounds: GridRequest):
    grid_points = []
    
    steps_lat = bounds.resolution
    steps_lng = int(bounds.resolution * 1.5) # Aspect ratio adjustment

    lat_step = (bounds.north - bounds.south) / steps_lat
    lng_step = (bounds.east - bounds.west) / steps_lng
    
    # Calculate radius for circles (in meters approx) for the frontend
    radius = (lat_step * 111000) / 2 * 1.2

    for i in range(steps_lat):
        for j in range(steps_lng):
            lat = bounds.south + (i * lat_step)
            lng = bounds.west + (j * lng_step)

            # CALL THE LOGIC (Now includes date_key)
            ndvi = calculate_ndvi_for_point(lat, lng, bounds.date_key)
            color = get_color_for_ndvi(ndvi)

            grid_points.append({
                "lat": lat,
                "lng": lng,
                "ndvi": round(ndvi, 2),
                "color": color,
                "radius": radius
            })

    return {"points": grid_points}

# 2. NEW API Endpoint: Seasonal/Yearly Stats
@app.get("/api/seasonal-stats")
async def get_seasonal_stats():
    # Define the comparison data keys for the last 2 years
    date_keys = [
        '2025-spring', '2025-summer', '2025-autumn', '2025-winter',
        '2024-spring', '2024-summer', '2024-autumn', '2024-winter',
    ]

    stats = {}
    for key in date_keys:
        stats[key] = calculate_regional_average_ndvi(key)
        
    # Structure the data for easy consumption by the frontend chart
    yearly_data = {
        2025: {
            'spring': stats['2025-spring'],
            'summer': stats['2025-summer'],
            'autumn': stats['2025-autumn'],
            'winter': stats['2025-winter'],
        },
        2024: {
            'spring': stats['2024-spring'],
            'summer': stats['2024-summer'],
            'autumn': stats['2024-autumn'],
            'winter': stats['2024-winter'],
        }
    }
    
    return yearly_data

# 3. Serve the Frontend
# Mount the frontend directory so we can serve the HTML file
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_path, "trnava-ndvi-monitor.html"))