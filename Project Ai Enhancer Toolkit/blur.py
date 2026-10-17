import cv2

def blur_image(image):
    """Apply a Gaussian blur to the image."""
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    
    return blurred_image