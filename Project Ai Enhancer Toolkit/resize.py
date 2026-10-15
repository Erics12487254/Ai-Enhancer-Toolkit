import cv2

# Resize workflow: receive a loaded image, resize it to 800 × 600, and return it.
def resize_image(image):
    resized_image = cv2.resize(image, (800, 600))

    return resized_image
