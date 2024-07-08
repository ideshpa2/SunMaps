# importing
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import geodatasets
import webbrowser
from folium import Popup, Tooltip
from folium.plugins import MarkerCluster


# loading data
phoenix = geodatasets.get_path("geoda.phoenix_acs")
gdf = gpd.read_file(phoenix)
gdfzoning = gpd.read_file("Zoning.shp")

# centering map
center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
phoenix_map = folium.Map(location=center, zoom_start=10)

folium.GeoJson(gdf).add_to(phoenix_map)

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


# saving map
phoenix_map.save("phoenix_interactive.html")
ax = gdfzoning.plot()
plt.savefig("zoning.png")

# opening
webbrowser.open("phoenix_interactive.html")
