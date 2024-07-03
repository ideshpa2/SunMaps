import geopandas as gpd

gdf = gpd.read_file('/Users/sofievargas/SunMaps/Zoning.shp')
gdf.explore("area", legend = True)
