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

# Create the map
fmap = folium.Map(location=[33.4484, -112.0740], zoom_start=10)

#Opening MRT data
tiff_path = "mrt_20120627_1300.tif"
dst_crs = 'EPSG:4326'

src = rasterio.open(tiff_path)
band = src.read(1)[::100, ::100]

transform, width, height = calculate_default_transform(
    src.crs, dst_crs, src.width, src.height, *src.bounds)
simplified_transform = from_origin(src.bounds.left, src.bounds.top, src.res[0] * 100, src.res[1] * 100)
simplified_data = band.tolist()

with open("simplified_mrt_data.json", "w") as f:
    json.dump({
        "transform": list(simplified_transform),
        "data": simplified_data
    }, f)

#LCZ image path and bounds
image_path = "2016_0504_LCZ_PHOENIX_filter_3x3.png"
lcz_bounds = [[32.651710000000001, -112.82271], [34.09861, -111.14831]]
image = Image.open(image_path)
lcz_width, lcz_height = image.size
print(lcz_width, lcz_height)


# Add the image overlay
image_overlay = ImageOverlay(
    name="LCZ",
    image=image_path,
    bounds=lcz_bounds,
    opacity=0.6
)
image_overlay.add_to(fmap)

mrt_overlay = folium.raster_layers.ImageOverlay(
    name = "MRT",
    image = "geotiff_image.png",
    bounds = [[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]],
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
