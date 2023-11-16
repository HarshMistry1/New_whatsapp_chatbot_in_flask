import webcolors
from PIL import Image
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def closest_color(rgb):
    differences = {}
    for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
        r, g, b = webcolors.hex_to_rgb(color_hex)
        differences[sum([(r - rgb[0]) ** 2,
                         (g - rgb[1]) ** 2,
                         (b - rgb[2]) ** 2])] = color_name

    return differences[min(differences.keys())]

def get_image_color_names(image_path, top_n=5):
    try:
        img = Image.open(image_path)
        img = img.resize((35, 35))

        # Get a list of color names and their counts
        colors = img.getcolors(img.size[0] * img.size[1])
        color_counts = {}
        for count, color in colors:
            rgb_color = color[:3]  # Extract RGB values
            color_name = closest_color(rgb_color)
            color_counts[color_name] = color_counts.get(color_name, 0) + count

        # Sort the colors by their counts in descending order
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

        # Return the top 'top_n' colors
        return [color_name for color_name, _ in sorted_colors[:top_n]]

    except Exception as e:
        return [("Error", str(e))]


def get_image_details(image):
    if isinstance(image, Image.Image):
        img_type = "PIL.Image.Image"
        color_channels = 1 if image.mode == "L" else 3
        data_type = "Unknown"  # PIL images do not have a 'dtype' attribute
    elif isinstance(image, np.ndarray):
        img_type = str(type(image))
        color_channels = image.shape[2] if len(image.shape) == 3 else 1
        data_type = image.dtype
    else:
        return "Invalid input image."

    return img_type, color_channels, data_type

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            ppi = img.info.get('dpi', (72.0, 72.0))
            return width, height, ppi
    except IOError:
        print(f"Error: Unable to open the image '{image_path}'")
        return None, None, None

def pixels_to_inches(pixels, ppi):
    inches = pixels / ppi
    return inches

# # Example usage:
# image_path = '/home/saubhagyam/Downloads/images (2).jpeg'
# image = Image.open(image_path)

# color_names = get_image_color_names(image_path)
# print("Color Names:", color_names)

# img_type, color_channels, data_type = get_image_details(image)
# print("Image Type:", img_type)
# print("Color Channels:", color_channels)
# # print("Data Type:", data_type)