import cv2 as cv
import numpy as np
import streamlit as st

# Function to remove the background using GrabCut
def remove_background(image):
    image=cv.cvtColor(image,cv.COLOR_RGB2BGR)
    copy = image.copy()
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Let the user select a region
    roi = cv.selectROI("Select Region", image, fromCenter=False, showCrosshair=True)
    cv.destroyAllWindows()  # Close the selection window
    x1, y1, x2, y2 = roi
    rect = (x1, y1, x2, y2)

    # Show the selected rectangle
    cv.rectangle(copy, (x1, y1), (x1 + x2, y1 + y2), (0, 0, 255), 1)
    cv.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    white_bg = np.full_like(image, 255)  # Create a white background
    image = np.where(mask2[:, :, np.newaxis] == 1, image, white_bg)  # Replace BG with white
    image=cv.cvtColor(image,cv.COLOR_BGR2RGB)

    return image

# Function to apply the sketch effect
def apply_sketch_effect(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)  # Enhance contrast

    # Inverting the Image
    invert_image = cv.bitwise_not(gray)

    # Apply Gaussian Blur to reduce noise
    blur = cv.GaussianBlur(invert_image, (25, 25), 0)

    # Inverting the Blurred Image
    invert_blur = cv.bitwise_not(blur)

    # Convert Image into Sketch
    sketch = cv.divide(gray, invert_blur, scale=256.0)
    return sketch

# Function to apply watercolor effect
def apply_watercolor_effect(image, sigma_s, sigma_r):
    return cv.stylization(image, sigma_s=sigma_s, sigma_r=sigma_r)

# Function to apply color sketch effect
def apply_color_sketch_effect(image, sigma_s, sigma_r,shade_factor):
    gray_sketch, color_sketch =cv.pencilSketch(image, sigma_s=sigma_s, sigma_r=sigma_r,shade_factor=shade_factor)
    return color_sketch
