import numpy as np

def crop_image(image):
    #Check the input type in case this function is called directly.
    if not isinstance(image, np.ndarray):
        raise TypeError("Input must be a NumPy array.")

    if image.shape[0] < 500 or image.shape[1] < 500:
        raise ValueError("Image is too small to crop. Minimum size is 500x500 pixels.")
    cropped_image = image[100:500, 100:500]  # Crop the image to a 400x400 region.

    return cropped_image

