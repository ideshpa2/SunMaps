import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#reflective pavement infrastructure
def pavement_infrastructure(lcz, mrt, zoning):
    lowrise_lczs = (
        
            "LCZ 9 (Sparsely Built)", 
            "LCZ D (Low Plants)",   
            "LCZ E (Bare rock or paved)"
    )
    highrise_lczs = (
            "LCZ 5 (Open Midrise)", 
            "LCZ 6 (Open Low Rise)",
            "LCZ 8 (Large Low-rise)",
            "LCZ 10 (Heavy Industry)"
    )
    if mrt > medians[lcz]:
        albedo = 0.7
    if mrt == medians[lcz]:
        albedo = 0.5
    if mrt < medians[lcz]:
        albedo = 0.3

    if lcz in lowrise_lczs:
        projected_mrt = mrt-27
    
    if lcz in  highrise_lczs:
        projected_mrt = mrt-14
    
    solution = f"For LCZ '{lcz}', MRT {mrt}, and zoning '{zoning}',we recommend that reflective pavement of a {albedo} albedo  would result in a projected mean radiant temperature  of {projected_mrt} °C"



#cool roof infrastructure
def cool_roof_infrastructure(lcz, mrt, zoning):
    best_lczs = (
            "LCZ 4 (Open High-rise)",
            "LCZ 5 (Open Midrise)", 
            "LCZ 7 (Lightweight Low-rise)", 
            "LCZ 8 (Large Low-rise)",
            "LCZ 10 (Heavy Industry)",
            "LCZ B (Scattered Trees)",
            "LCZ D (Low Plants)" 
    )
    if lcz in best_lczs and zoning == "residential":
        projected_mrt = mrt-0.3
    
    return f"For LCZ '{lcz}', MRT {mrt}, and zoning '{zoning}',recommended cool roofs would result in a projected mean radiant temperature  of {mrt - 8.2} °C"

#water_mister_infrastructure
def water_mister_infrastructure(lcz, mrt, zoning):
    best_lczs = (
            "LCZ 4 (Open High-rise)",
            "LCZ 5 (Open Midrise)", 
            "LCZ 7 (Lightweight Low-rise)", 
            "LCZ 8 (Large Low-rise)",
            "LCZ 10 (Heavy Industry)"
    )
    if(lcz in best_lczs):
        if(zoning == 'commercial' or zoning == 'industrial'):
            solution = f"For LCZ '{lcz}', MRT {mrt}, and zoning '{zoning}',recommended water misters would result in a projected mean radiant temperature  of {mrt - 8.2} °C"
    return solution
        
#Tree Canopy "Table"
        
def tree_canopy_infrastructure(lcz, mrt, zoning):
    #trees work best in low rise, low density neighborhoods
    projected_mrt = mrt
    best_lczs = (
        "LCZ 6 (Open Low Rise)",
        "LCZ 7 (Lightweight Low-rise)", 
        "LCZ 8 (Large Low-rise)",
        "LCZ 9 (Sparsely Built)" 
        )

    
    if lcz in best_lczs:
        if mrt > medians[lcz]:
            tree_type = "Non-native deciduous and evergreen trees"
            projected_mrt-=13
        elif mrt == medians[lcz]:
            tree_type = "Native trees"
            projected_mrt -= 8.8
        else:
            tree_type = "Phoenix Palm trees"
            projected_mrt -= 5.6

    percentage = 0
    tree_type = ""
    if(zoning == "commercial"):
        percentage = 15
    if(zoning == "industrial"):
        percentage = 10
    if(zoning == "residential"):
        percentage = 25
    
    solution += f"For LCZ '{lcz}', MRT {mrt}, and zoning '{zoning}', we recommend a {percentage}% increase in tree canopy cover with {tree_type}, with a projeted mean radiant temperature of {projected_mrt} °C."
    return solution



# Load your data
with open('lcz_mrt_data.json', 'r') as f:
    lcz_mrt_data = json.load(f)



# Create plots for each LCZ
means = {}
for lcz, mrts in lcz_mrt_data.items():
    mrts_non_zero = [mrt for mrt in mrts if mrt != 0]
    mrt_mean = np.mean(mrts_non_zero)
    mrt_median = np.median(mrts_non_zero)
    mrt_range = (min(mrts_non_zero), max(mrts_non_zero))
    means[lcz] = mrt_mean
    print(lcz, ": " , means[lcz], ",")






"""
    print(lcz)
    plt.figure(figsize=(10, 6))
    sns.histplot(mrts_non_zero, kde=True)  # kde=True to add the kernel density estimate (bell curve)

    # Add vertical lines for mean and median
    plt.axvline(mrt_mean, color='r', linestyle='--', linewidth=1, label=f'Mean: {mrt_mean:.2f}')
    plt.axvline(mrt_median, color='g', linestyle='-', linewidth=1, label=f'Median: {mrt_median:.2f}')
    
    # Add text annotations for range, mean, and median
    plt.text(mrt_mean, plt.ylim()[1]*0.9, f'Mean: {mrt_mean:.2f}', color='r', ha='center')
    plt.text(mrt_median, plt.ylim()[1]*0.8, f'Median: {mrt_median:.2f}', color='g', ha='center')
    plt.text(mrt_range[0], plt.ylim()[1]*0.7, f'Range: {mrt_range[0]:.2f} - {mrt_range[1]:.2f}', color='b', ha='left')

    plt.title(f'MRT Distribution for LCZ {lcz}')
    plt.xlabel('Mean Radiant Temperature')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(f"mrt_distributions/{lcz}_distribution.png")


/Users/sofievargas/SunMaps-2/mrt_distributions
import json
import requests
from PIL import Image
image = Image.open("2016_0504_LCZ_PHOENIX_filter_3x3.png")

with open('simplified_mrt_data.json', 'r') as file:
    data = json.load(file)
mrtData = data['data']
transform = data['transform']

lcz_image = Image.open("2016_0504_LCZ_PHOENIX_filter_3x3.png")
lcz_pixels = lcz_image.load()
lcz_img_size = lcz_image.size
lczbounds = [
    (32.651710000000001, -112.82271), 
    (34.09861, -111.14831)
]

def map_to_image_coords(lat, lon, bounds, imageSize):
        latMin = bounds[0][0]
        lonMin = bounds[0][1]
        latMax = bounds[1][0]
        lonMax = bounds[1][1]
        imgWidth = imageSize[0]
        imgHeight = imageSize[1]
        x = round((lon - lonMin) / (lonMax - lonMin) * imgWidth)
        y = round((latMax - lat) / (latMax - latMin) * imgHeight)
        return x, y


def map_to_mrt_coords(lat, lon, transform):
    a = transform[0]
    b = transform[1]
    c = transform[2]
    d = transform[3]
    e = transform[4]
    f = transform[5]
    col = round((lon - c) / a)
    row = round((lat - f) / e)
    return row, col

def get_color_from_image(image, x, y):
    print('getColorFromImage called with:', x, y)
    image_data = image.load()
    color = image_data[x, y]
    print('Extracted color:', color)
    result = f"{color[0]},{color[1]},{color[2]}"
    return result

def color_to_zone(color):
    color_to_zone_mapping = {
        "140,0,0": "LCZ 4 (Open High-rise)",
        "209,0,0": "LCZ 5 (Open Midrise)",    
        "255,0,0": "LCZ 6 (Open Low Rise)",
        "0,106,0": "LCZ A (Dense Trees)",
        "0,170,0": "LCZ B (Scattered Trees)",
        "100,133,37": "LCZ C (Bush, Scrub)",
        "185,219,121": "LCZ D (Low Plants)",
        "0,0,0": "LCZ E (Bare rock or paved)", 
        "251,247,174": "LCZ F (Bare Soil or Sand)", 
        "106,106,255": "LCZ G (Water)", 
        "191,77,0": "LCZ 4 (Open High-rise)",
        "255,102,0": "LCZ 5 (Open Midrise)", 
        "255,153,85": "LCZ 6 (Open Low Rise)",
        "250,238,5": "LCZ 7 (Lightweight Low-rise)", 
        "188,188,188": "LCZ 8 (Large Low-rise)",
        "255,204,170": "LCZ 9 (Sparsely Built)", 
        "85,85,85": "LCZ 10 (Heavy Industry)"
    }
    zone = color_to_zone_mapping.get(color, "Unknown")
    print('Mapped color to zone:', zone)
    return zone
lcz_mrt_map = {}
height = len(mrtData)
width = len(mrtData[0])
for i in range(height):
    for j in range(width) :
        lon = transform[0] * j + transform[2]
        lat = transform[4] * i + transform[5]
        
        mrt = mrtData[i][j]
        lczx, lczy = map_to_image_coords(lat, lon, lczbounds, lcz_img_size)
        lcz = color_to_zone(get_color_from_image(image, lczx, lczy))
        if lcz not in lcz_mrt_map:
            lcz_mrt_map[lcz] = []
        lcz_mrt_map[lcz].append(mrt)

lcz_mrt_data_str = "data:text/json;charset=utf-8," + json.dumps(lcz_mrt_map)
with open("lcz_mrt_data.json", "w") as f:
    f.write(json.dumps(lcz_mrt_map))"""
