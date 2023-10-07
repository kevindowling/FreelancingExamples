import cv2
import numpy as np
from pdf2image import convert_from_path
from matplotlib import pyplot as plt

# Step 1: PDF to Image Conversion
def pdf_to_image_list(pdf_path):
    images = convert_from_path(pdf_path)
    return images

#display the images from the pdf file
def display_images(images):
    for i, image in enumerate(images):
        plt.figure()
        plt.imshow(image)
        plt.title(f'Page {i + 1}')
        plt.axis('off')  # Hide axes
        plt.show()

# Step 2: Shape Detection
def detect_shapes(image):
    # Convert PIL Image to NumPy array
    image_np = np.array(image)
    # Convert image to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # Find contours
    # apply binary thresholding
    ret, thresh = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)
    # visualize the binary image
    cv2.waitKey(0)
    cv2.imwrite('image_thres1.jpg', thresh)
    cv2.destroyAllWindows()
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    contours_first_removed = []
    for contour in contours: 
        if(i == 0):
            i += 1
            continue

        contours_first_removed.append(contour)
        


    return contours_first_removed


# Step 3: Shape Uniqueness Evaluation
def evaluate_uniqueness(contours):
    # Placeholder function. You'll need to implement your uniqueness heuristic
    unique_contours = contours  # This is a stub. Replace with your logic.
    return unique_contours

# Step 4: Visualization
def visualize_shapes(unique_contours):
    for i, contour in enumerate(unique_contours):
        # Get dimensions from the first image in your image list
        width, height = images[0].size  # assuming images is a global variable or pass it as an argument
        # Create a blank white image with the same dimensions as your original image
        blank_image = np.ones((height, width, 3), dtype=np.uint8) * 255
        # Draw each contour on the blank image with a thicker line
        cv2.drawContours(blank_image, [contour], -1, (0,255,0), 10)  # changed line thickness to 10
        plt.figure()
        plt.imshow(cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB))
        plt.title(f'Shape {i + 1}')
        plt.show()