# importing
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import geodatasets
import webbrowser

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

# saving map
phoenix_map.save("phoenix_interactive.html")
ax = gdfzoning.plot()
plt.savefig("zoning.png")

# opening
webbrowser.open("phoenix_interactive.html")
