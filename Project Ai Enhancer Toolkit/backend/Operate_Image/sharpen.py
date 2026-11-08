import cv2
import numpy as np

def sharpen_image(image):
    """Apply a sharpening filter to the image."""
    # Define a sharpening kernel.
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]], 
                       dtype=np.float32) #tells NumPy to store the kernel numbers as 32-bit floating-point values
    
    # Apply the kernel to the image using filter2D.
    #-1: keep the output image’s data depth the same 
    # as the input’s. It is not a kernel value.
    #filter2D() returns a processed image, 
    # which is assigned to sharpened_image
    sharpened_image = cv2.filter2D(image, -1, kernel) 

    return sharpened_image

#Test purpose only.
#print("original image shape:", image.shape)
#print("sharpened image shape:", sharpened_image.shape)
#print("Are they identical?", np.array_equal(image, sharpened_image))  # Check if the original and sharpened images are identical.