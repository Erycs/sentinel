import rioxarray as rxr
import matplotlib.pyplot as plt

# --- 1. načítanie dát ---
nir = rxr.open_rasterio("B8_2022.tif").squeeze()
red = rxr.open_rasterio("B4_2022.tif").squeeze()

# --- 2. výpočet NDVI ---
ndvi = (nir - red) / (nir + red)

# --- 3. zobrazenie ---
plt.imshow(ndvi, cmap="RdYlGn")
plt.colorbar(label="NDVI")
plt.title("NDVI 2022")
plt.show()
