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


#Census Heat Morbidities
gdf_hm = gpd.read_file("datasets_geographic/Heat_morbidities_by_census_tract_2012_to_2016.shp")[['Shape_Area','MORBIDNUM','geometry']]
print("heat morbidities: \n", gdf_hm.head())


#UV index by Zip Code
gdf_zipcodes = gpd.read_file("Zip_Code_Stuff/Zip_Codes.shp")[['ZCTA5CE10','geometry']]
gdf_zipcodes = gdf_zipcodes.rename(columns = {"ZCTA5CE10": "ZIP", "geometry": "geometry"})#.dropna(subset = ['UV_VALUE'], inplace = True)
uv = testscikit.zdf
gdf_zipcodes = gdf_zipcodes.merge(uv, on="ZIP")
print(gdf_zipcodes.head())


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

#putting datasets on the GUI
##uv index
folium.Choropleth(    
    geo_data = gdf_zipcodes,
    name = 'UV Index',
    data = gdf_zipcodes,
    columns=['ZIP','UV_VALUE'],
    nan_fill_color='purple',
    key_on="feature.properties.ZIP",
    fill_color = 'OrRd',
    fill_opacity = 0.8,
    line_opacity=0.2,
    legend_name='Average UV Value',
    smooth_factor=0).add_to(phoenix_map)
##heat morbidities
folium.Choropleth(    
    geo_data = gdf_hm,
    name = 'Heat Morbidity',
    data = gdf_hm,
    columns=['Shape_Area','MORBIDNUM'],
    nan_fill_color='green',
    key_on="feature.properties.Shape_Area",
    fill_color = 'RdPu',
    bins = [0,5,15,30,45,60,100,200,340],
    fill_opacity = 0.8,
    line_opacity=0.2,
    legend_name='Heat Morbidities',
    smooth_factor=0).add_to(phoenix_map)

#adding interactivity
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
uv_highlights = folium.features.GeoJson(
    gdf_zipcodes,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['ZIP','UV_VALUE'],
        aliases=['Zip Code: ','Average UV Index: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
heatd_highlights = folium.features.GeoJson(
    gdf_hm,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Shape_Area','MORBIDNUM'],
        aliases=['Area: ','Heat Morbidities: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
phoenix_map.add_child(heatd_highlights)
phoenix_map.keep_in_front(heatd_highlights)
phoenix_map.add_child(uv_highlights)
phoenix_map.keep_in_front(uv_highlights)

# saving map
folium.LayerControl().add_to(phoenix_map)
phoenix_map.save("phoenix_interactive.html")
ax = gdfzoning.plot()
plt.savefig("zoning.png")

# opening
webbrowser.open("phoenix_interactive.html")

