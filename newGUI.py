import folium
from folium.raster_layers import ImageOverlay
from PIL import Image
import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.transform import from_origin
import webbrowser
from matplotlib import pyplot
import json
import numpy as np
from collections import defaultdict

#satellite map tile
attr = (
    '&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)
tiles = "https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.jpg"

# Create the map
fmap = folium.Map(
                max_bounds=True,
                location=[33.4484, -112.0740],
                tiles = tiles, 
                attr = attr, 
                zoom_start=15,
                min_lat=33.23,
                max_lat=33.68,
                min_lon=-111.83,
                max_lon=-112.44,
                )


# Add the image overlay
image_overlay = ImageOverlay(
    name="LCZ",
    image="2016_0504_LCZ_PHOENIX_filter_3x3.png",
    bounds=[[32.651710000000001, -112.82271], [34.09861, -111.14831]],
    opacity=0.6
)
image_overlay.add_to(fmap)

mrt_overlay = folium.raster_layers.ImageOverlay(
    name = "MRT",
    image = "geotiff_image.png",
    bounds = [[33.23, -112.44], [33.68 , -111.83]],
    opacity = 0.6
)
mrt_overlay.add_to(fmap)

folium.LayerControl().add_to(fmap)

fmap.save("lcz.html")

with open("lcz.html", "r") as f:
    lines = f.readlines()

# Insert the JavaScript link before the closing </body> tag
for i, line in enumerate(lines):
    if "</body>" in line:
        lines.insert(i, '<script src="popup.js"></script>\n')
        break

# Write the modified HTML back to the file
with open("lcz.html", "w") as f:
    f.writelines(lines)

# Embed the MRT data, transform, and image path in the JavaScript file
with open("popup.js", "r") as f:
    js_content = f.read()

with open("popup.js", "w") as f:
    f.write(js_content)

# Open the map in the browser
webbrowser.open("lcz.html")


###Get MRT Distribution and Percentile
with open('simplified_mrt_data.json', 'r') as file:
    mrt_data = json.load(file)

transform = mrt_data['transform']
mrt_values = np.array(mrt_data['data'])

def geographic_to_pixel(lon, lat, transform):
    x_pixel = int((lon - transform[2]) / transform[0])
    y_pixel = int((lat - transform[5]) / transform[4])
    return x_pixel, y_pixel

def get_lcz_from_coords(lon, lat):
    # Implement this function to get LCZ based on lon/lat
    pass

# Dictionary to store MRT values for each LCZ
lcz_mrt_dict = defaultdict(list)

# Iterate over the MRT data and map to LCZ
rows, cols = mrt_values.shape
for x in range(cols):
    for y in range(rows):
        lon = transform[0] * x + transform[2]
        lat = transform[4] * y + transform[5]
        mrt = mrt_values[y, x]
        lcz = get_lcz_from_coords(lon, lat)
        lcz_mrt_dict[lcz].append(mrt)

# Calculate percentiles for each LCZ
lcz_percentiles = {}
for lcz, mrt_values in lcz_mrt_dict.items():
    if mrt_values:
        lcz_percentiles[lcz] = np.percentile(mrt_values, [25, 50, 75, 90, 95])

# Example of how to find the percentile of a new MRT value
def find_mrt_percentile(lcz, mrt_value):
    if lcz not in lcz_mrt_dict or not lcz_mrt_dict[lcz]:
        return None
    mrt_values = lcz_mrt_dict[lcz]
    return np.sum(mrt_values <= mrt_value) / len(mrt_values) * 100

def find_mrt_percentile(lcz, mrt_value):
    if lcz not in lcz_mrt_dict or not lcz_mrt_dict[lcz]:
        return None
    mrt_values = lcz_mrt_dict[lcz]
    return np.sum(mrt_values <= mrt_value) / len(mrt_values) * 100