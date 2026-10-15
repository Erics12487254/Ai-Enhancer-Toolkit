import cv2

# Load an image for processing and report when OpenCV cannot decode it.
def load_image(path):
    image = cv2.imread(path)
    
    if image is None:
        raise ValueError(f"Could not load image: {path}")
    
    return image
