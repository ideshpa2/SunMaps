# importing
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium
import geodatasets
import webbrowser
from folium import Popup, Tooltip
from folium.plugins import MarkerCluster
import branca.colormap as cm
import testscikit

# loading data
phoenix = geodatasets.get_path("geoda.phoenix_acs")
gdf = gpd.read_file(phoenix)
gdfzoning = gpd.read_file("Zoning.shp")

#UV index by Zip Code
gdf_zipcodes = gpd.read_file("Zip_Code_Stuff/Zip_Codes.shp")[['ZCTA5CE10','geometry']]
gdf_zipcodes = gdf_zipcodes.rename(columns = {"ZCTA5CE10": "ZIP", "geometry": "geometry"})#.dropna(subset = ['UV_VALUE'], inplace = True)
uv = testscikit.zdf
print(gdf_zipcodes)

gdf_zipcodes = gdf_zipcodes.merge(uv, on="ZIP")
print(gdf_zipcodes.head())

# centering map
center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
phoenix_map = folium.Map(location=center, zoom_start=10)


folium.GeoJson(gdf).add_to(phoenix_map)
folium.GeoJson(gdf_zipcodes).add_to(phoenix_map)
# coords for most walkable phx area
marker_location = [33.4484, -112.0740]

# marking location
folium.Marker(location=marker_location,
              popup='testing').add_to(phoenix_map)
# html code for popup
popup_content = """
<div style="width:200px">
    <h4>Testing</h4>
    <p>menu options.</p>
    <label for="pages">Choose a page:</label>
    <select id="pages" name="pages" onchange="location = this.value;">
        <option value="">Select...</option>
        <option value="https://example.com/page1">page 1</option>
        <option value="https://example.com/page2">page 2</option>
        <option value="https://example.com/page3">page 3</option>
    </select>
</div>
"""
tooltip_content = "click for info"

folium.Marker(
    location=marker_location,
    popup=Popup(popup_content, max_width=300),
    tooltip=Tooltip(tooltip_content)
).add_to(phoenix_map)

#putting UV data on the GUI
folium.Choropleth(    
    geo_data = gdf_zipcodes,
    name = 'Choropleth',
    data = gdf_zipcodes,
    columns=['ZIP','UV_VALUE'],
    nan_fill_color='purple',
    key_on="feature.properties.ZIP",
    fill_color = 'OrRd',
    fill_opacity = 1,
    line_opacity=0.2,
    legend_name='Average UV Value',
    smooth_factor=0).add_to(phoenix_map)

# saving map

folium.LayerControl().add_to(phoenix_map)
phoenix_map.save("phoenix_interactive.html")
ax = gdfzoning.plot()
plt.savefig("zoning.png")

# opening
webbrowser.open("phoenix_interactive.html")

