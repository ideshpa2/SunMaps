import folium
import zipfile
import io
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
import xml.etree.ElementTree as ET
from pyproj import Proj, transform


def read_geotiff(file_path):
    # Open the GeoTIFF file
    with rasterio.open(file_path) as src:
        # Read the data
        data = src.read(1)  # Reading the first band
        bounds = src.bounds  # Get the bounds of the raster
    print(f"GeoTIFF Bounds: {bounds}")
    print(f"Data type: {data.dtype}")
    print(f"Data shape: {data.shape}")
    print(f"Min MRT value: {np.min(data)}")
    print(f"Max MRT value: {np.max(data)}")
    return data, bounds

def save_geotiff_image(data, output_file='geotiff_image.png'):
    # Normalize the data for visualization
    norm = Normalize(vmin=np.min(data), vmax=np.max(data))
    data_normalized = norm(data)
    
    # Create an image from the normalized data
    plt.imshow(data_normalized, cmap='hot')
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    plt.close()

def geotiff_overlay_bounds(bounds):
    in_proj = Proj(init='epsg:26912')
    out_proj = Proj(init='epsg:4326')
    
    bottom_left = transform(in_proj, out_proj, bounds.left, bounds.bottom)
    top_right = transform(in_proj, out_proj, bounds.right, bounds.top)
    
    image_bounds = [
        [bottom_left[1], bottom_left[0]],  # Bottom-left corner in lat/lon
        [top_right[1], top_right[0]]       # Top-right corner in lat/lon
    ]
    
    print(f"Converted GeoTIFF Overlay Bounds: {image_bounds}")  # Debug: Print converted bounds
    return image_bounds

def kml_overlay_bounds(kml_file_path):
    tree = ET.parse(kml_file_path)
    root = tree.getroot()
    
    # Namespace used in the KML file
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Extract coordinates from the KML file
    lat_lon_box = root.find('.//kml:LatLonBox', namespace)
    north = float(lat_lon_box.find('kml:north', namespace).text)
    south = float(lat_lon_box.find('kml:south', namespace).text)
    east = float(lat_lon_box.find('kml:east', namespace).text)
    west = float(lat_lon_box.find('kml:west', namespace).text)
    
    # Define the bounds for the image overlay
    image_bounds = [
        [south, west],  # Bottom-left corner
        [north, east]   # Top-right corner
    ]
    return image_bounds

# Path to your PNG, KML, and GeoTIFF files
png_file_path = '2016_0504_LCZ_PHOENIX_filter_3x3.png'
kml_file_path = '2016_0504_LCZ_PHOENIX_filter_3x3.kml'
geotiff_file_path = 'mrt_20120627_1300.tif'

# Create the map with the LCZ and MRT overlay
map = folium.Map(location=[33.4484, -112.0740], zoom_start=10)

# Get KML overlay bounds
kml_bounds = kml_overlay_bounds(kml_file_path)

# Add the KML image overlay to the map
folium.raster_layers.ImageOverlay(
    name='KML Overlay',
    image=png_file_path,
    bounds=kml_bounds,
    opacity=0.3,
    interactive=True
).add_to(map)

# Read the GeoTIFF data
geotiff_data, geotiff_bounds = read_geotiff(geotiff_file_path)

# Save the GeoTIFF data as an image
geotiff_image_file = 'geotiff_image.png'
save_geotiff_image(geotiff_data, geotiff_image_file)

# Get GeoTIFF overlay bounds
geotiff_image_bounds = geotiff_overlay_bounds(geotiff_bounds)

# Add the GeoTIFF image overlay to the map
folium.raster_layers.ImageOverlay(
    name='GeoTIFF Overlay',
    image='geotiff_image.png',
    bounds=geotiff_image_bounds,
    opacity=0.3,
    interactive=True
).add_to(map)

# Add a layer control panel
folium.LayerControl().add_to(map)

# Save the map to an HTML file
map.save('lcz.html')

