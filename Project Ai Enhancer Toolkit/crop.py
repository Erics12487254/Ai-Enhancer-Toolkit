import cv2

def crop_image(image):
    cropped_image = image[100:500, 100:500]  # Crop the image to a 400x400 region.

    return cropped_image

