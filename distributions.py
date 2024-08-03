import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your data
with open('lcz_mrt_data.json', 'r') as f:
    lcz_mrt_data = json.load(f)



# Create plots for each LCZ
for lcz, mrts in lcz_mrt_data.items():
    mrts_non_zero = [mrt for mrt in mrts if mrt != 0]
    mrt_mean = np.mean(mrts_non_zero)
    mrt_median = np.median(mrts_non_zero)
    mrt_range = (min(mrts_non_zero), max(mrts_non_zero))


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

"""
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
    f.write(json.dumps(lcz_mrt_map))






import json
from collections import defaultdict
from PIL import Image
lcz_mrt_data = defaultdict(list)
import matplotlib.pyplot as plt
import os

lcz_image = Image.open("2016_0504_LCZ_PHOENIX_filter_3x3.png")
lcz_pixels = lcz_image.load()

def map_to_image_coords(lat, lon, bounds, imageSize) {
        latMin = bounds[0][0], lonMin = bounds[0][1], latMax = bounds[1][0], lonMax = bounds[1][1]
        imgWidth = imageSize[0], imgHeight = imageSize[1]
        x = Math.round((lon - lonMin) / (lonMax - lonMin) * imgWidth)
        y = Math.round((latMax - lat) / (latMax - latMin) * imgHeight)
        return x, y
    }

with open('simplified_mrt_data.json', 'r') as file:
    mrtjson = json.load(file)

transform = mrtjson['transform']
mrt_data = mrtjson['data']

def pixel_to_geo(transform, px, py):
    a, b, c, d, e, f = transform[0], transform[1], transform[2], transform[3], transform[4], transform[5]
    lon = a * px + b * py + c
    lat = d * px + e * py + f
    return lon, lat

print(pixel_to_geo(transform, 300, 300))

LCZ = {
        (140,0,0): "LCZ 4 (Open High-rise)",
        (209,0,0): "LCZ 5 (Open Midrise)",    
        (255,0,0): "LCZ 6 (Open Low Rise)" ,
        (0,106,0): "LCZ A (Dense Trees)",
        (0,170,0): "LCZ B (Scattered Trees)",
        (100,133,37): "LCZ C (Bush, Scrub)",
        (185,219,121): "LCZ D (Low Plants)",
        (0,0,0): "LCZ E (Bare rock or paved)", 
        (251,247,174): "LCZ F (Bare Soil or Sand)", 
        (106,106,255): "LCZ G (Water)", 
        (191,77,0): "LCZ 4 (Open High-rise)",            
        (255,102,0): "LCZ 5 (Open Midrise)", 
        (255,153,85): "LCZ 6 (Open Low Rise)",
        (250,238,): "LCZ 7 (Lightweight Low-rise)", 
        (188,188,188): "LCZ 8 (Large Low-rise)",
        (255,204,170): "LCZ 9 (Sparsely Built)", 
        (85,85,85): "LCZ 10 (Heavy Industry)"
}

height = len(mrt_data)
width = len(mrt_data[0])
lcz_mrt_data = defaultdict(list)
print(height, width)

for x in range(width):
    for y in range(height):
        val = mrt_data[y][x]
        if val != 0:
            lon, lat = pixel_to_geo(transform, x, y)
            lcz_x, lcz_y = int((lon-transform[2]) / transform[0]), int((lat - transform[5]) / transform[4])
        # Get the color of the current pixel
            color = lcz_pixels[x, y]
            if 0 <= lcz_x < lcz_image.width and 0 <= lcz_y < lcz_image.height:
                color = lcz_pixels[lcz_x, lcz_y]
                lcz_val = LCZ.get(color)
                if lcz_val:
                    lcz_mrt_data[lcz_val].append(val)

print("mrt data iterated")
print(len(lcz_mrt_data))
output_dir = 'mrt_distributions'
os.makedirs(output_dir, exist_ok=True)

# Create a histogram for each LCZ
counter = 0
for lcz, mrt_values in lcz_mrt_data.items():
    counter += 1
    plt.figure()
    plt.hist(mrt_values, bins=30, alpha=0.75, color='blue', edgecolor='black')
    plt.title(f'MRT Distribution for {lcz}')
    plt.xlabel('MRT')
    plt.ylabel('Frequency')
    plt.grid(True)
    file_path = os.path.join(output_dir, f"{counter}distribution.png")
    print(file_path)
    plt.savefig(f"{counter}distribution.png")
    plt.show()

print("distributions saved")"""