import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import geodatasets
import webbrowser
phoenix = geodatasets.get_path("geoda.phoenix_acs ")
gdfzoning = gpd.read_file("Zoning.shp")
gdf = gpd.read_file(phoenix)
map = gdf.plot()
zoningmap = gdfzoning.explore()
zoningmap.save("zoning.html")
interactivemap = gdf.explore()
plt.show()
interactivemap.save("phoenix.html")