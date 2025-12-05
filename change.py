import rioxarray as rxr
import matplotlib.pyplot as plt

# NDVI rok 1
nir1 = rxr.open_rasterio("B8_2022.tif").squeeze()
red1 = rxr.open_rasterio("B4_2022.tif").squeeze()
ndvi1 = (nir1 - red1) / (nir1 + red1)

# NDVI rok 2
nir2 = rxr.open_rasterio("B8_2024.tif").squeeze()
red2 = rxr.open_rasterio("B4_2024.tif").squeeze()
ndvi2 = (nir2 - red2) / (nir2 + red2)

# Rozdiel
delta = ndvi2 - ndvi1

plt.imshow(delta, cmap="RdYlGn")
plt.colorbar(label="NDVI change")
plt.title("NDVI change 2022 → 2024")
plt.show()
