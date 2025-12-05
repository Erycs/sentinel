from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from sentinel.ndvi_logic import calculate_ndvi_for_point, get_color_for_ndvi

app = FastAPI()

# Input model for the grid request
class GridRequest(BaseModel):
    north: float
    south: float
    east: float
    west: float
    resolution: int

# 1. API Endpoint: Calculate Grid
# We calculate the whole grid in Python to save the frontend from doing math
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

            # CALL THE LOGIC (This is where you'd call Sentinel API later)
            ndvi = calculate_ndvi_for_point(lat, lng)
            color = get_color_for_ndvi(ndvi)

            grid_points.append({
                "lat": lat,
                "lng": lng,
                "ndvi": round(ndvi, 2),
                "color": color,
                "radius": radius
            })

    return {"points": grid_points}

# 2. Serve the Frontend
# Mount the frontend directory so we can serve the HTML file
# Note: We look one level up (..) to find frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_path, "trnava-ndvi-monitor.html"))