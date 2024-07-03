import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import geodatasets
import webbrowser
phoenix = geodatasets.get_path("geoda.phoenix_acs ")
print(phoenix)
gdf = gpd.read_file(phoenix)
map = gdf.plot()
interactivemap = gdf.explore()
plt.show()
interactivemap.save("phoenix.html")