import streamlit as st
import requests
import numpy as np
from io import BytesIO
from PIL import Image
from morecolors import get_image_color_names, get_image_details,get_image_dimensions,pixels_to_inches
import cv2
import base64
from PIL import Image
from io import BytesIO


st.title('Image Detection')


def get_image():
    image = 'https://saubhagyam.com/public/assets/images/LOGO/Logo.jpg'
    new_image = requests.get(image)

    # Split the data URL to extract the Base64 part
    base64_image_data = base64_image.split(",")[1]

    # Decode the Base64 data
    image_data = base64.b64decode(base64_image_data)
    one_image = BytesIO(image_data)
    # one_image = BytesIO(new_image.content)
    return one_image

# st.image(get_image())

# genere = st.radio(
    # "how you want to upload your image",
    # ("Browse Photo","Camera"))

# if genere == "Camera":
    # uploaded_image = st.camera_input("Take a image")
# else:
    # uploaded_image = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])


# if uploaded_image is not None:
#         # Display the uploaded image
#         # st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

#         # Convert the image to a format compatible with PIL and OpenCV
#         pil_image = Image.open(uploaded_image)
#         opencv_image = np.array(pil_image)
#         opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

#         # Image processing code (You can add any processing you want here)

#         # Save the processed image using PIL
#         # st.write("Processed Image")
#         # st.image(pil_image, caption="Processed Image", use_column_width=True)

#         # Save the processed image using OpenCV
#         # save_button = st.button("Save Processed Image")
#         # if save_button:
#             # Provide a file path to save the image
#         save_path = "processed_image.jpg"  # You can change the file format or filename here
#         cv2.imwrite(save_path, opencv_image)
#         st.success(f"Image saved as {save_path}"

# if uploaded_image is not None:
#         # Display the uploaded image
#         # st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

#         # Convert the image to a format compatible with PIL and OpenCV
  

#         # Image processing code (You can add any processing you want here)

#         # Save the processed image using PIL
#         # st.write("Processed Image")
#         # st.image(pil_image, caption="Processed Image", use_column_width=True)

#         # Save the processed image using OpenCV
#         # save_button = st.button("Save Processed Image")
#         # if save_button:
#             # Provide a file path to save the image
#         save_path = "processed_image.jpg"  # You can change the file format or filename here
#         cv2.imwrite(save_path, opencv_image)
#         st.success(f"Image saved as {save_path}")
# # st.image(ImagePath)

# if st.button('Predict'):
#     mainimg = cv2.imread("processed_image.jpg")
#     height, width, _ = mainimg.shape
#     total_pixels = height * width
#     # image_dimensionality = get_image_dimensionality(mainimg)
    

#     # st.write("Image Dimensionality:", image_dimensionality)
#     st.write("Image Width: ", width)
#     st.write("Image Height: ", height)
#     st.write("Total Pixels: ", total_pixels)



uploaded_image = get_image()

if uploaded_image is not None:
    try:
        # Use PIL's Image.open() directly on the file-like object
        image1= Image.open(uploaded_image)
        st.image(image1)

        pil_image = Image.open(uploaded_image)
        opencv_image = np.array(pil_image)
        main_image = cv2.resize(opencv_image, (516, 516))
        # opencv_image = np.reshape(opencv_image, (3, 516, 516))
        opencv_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2RGB)

        save_path = "processed_image.jpg"  # You can change the file format or filename here
        cv2.imwrite(save_path, opencv_image)
        st.success(f"Image saved as {save_path}")

        if st.button('Predict'):
            main_image = cv2.imread("processed_image.jpg")
            height, width, _ = main_image.shape
            total_pixels = height * width
            # image_dimensionality = get_image_dimensionality(mainimg)
            

            # value = st.slider('Select a value', 1, 10, 5)

            # # Perform some processing based on the slider value
            # result = value * 2

            # # Display the result using st.write
            # st.write(f'Result: {result}')

            # st.write("Image Dimensionality:", image_dimensionality)

            width, height, ppi = get_image_dimensions(uploaded_image)
            if width is not None and height is not None and ppi is not None:
                st.write(f"Image width: {width} pixels")
                st.write(f"Image height: {height} pixels")
                st.write(f"Image width: {pixels_to_inches(width, ppi[0]):.2f} inches")
                st.write(f"Image height: {pixels_to_inches(height, ppi[1]):.2f} inches")
                st.write(f"Total Resolution {width*height}")
            # st.write("Image Width: ", width)
            # st.write("Image Height: ", height)
            # st.write("Total Pixels: ", total_pixels)



            img_type, color_channels, data_type = get_image_details(image1)
            # st.write("Image Width: ", width)
            # st.write("Image Height: ", height)
            # st.write("Total Pixels: ", total_pixels)
            # st.write("Image Type:", img_type)
            # st.write("color channel", color_channels)
            # st.write("Data Type:", data_type)

            top_colors = get_image_color_names(uploaded_image,top_n=5)
            # print("Top 5 dominant colors:", top_colors)
            color_join = ", ".join(map(str,top_colors))
            # st.write("color in image:",color_join)
            st.success(f"Image colors are: {color_join}")


        # if st.button('Predict'):
        #     # Perform additional image processing or analysis here if needed
        #     st.write("Prediction Results:")
        #     # Add your prediction logic here and display the results

    except Exception as e:
        st.write(f"Error: {str(e)}")