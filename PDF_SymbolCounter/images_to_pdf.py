from fpdf import FPDF
from PIL import Image
import io
import numpy as np
import cv2

def tuple_to_pil_image(contour_tuple, image_shape, line_thickness=2, line_color=(0, 255, 0)):
    """
    Converts a contour represented as a tuple to a PIL Image.
    
    Args:
    - contour_tuple (tuple): The contour represented as a tuple.
    - image_shape (tuple): The shape of the original image as (height, width, channels).
    - line_thickness (int, optional): The thickness of the contour line. Default is 2.
    - line_color (tuple, optional): Color of the contour line in BGR format. Default is green (0, 255, 0).

    Returns:
    - PIL.Image: A PIL Image with the contour drawn.
    """
    
    # Convert the contour tuple back to its original shape
    contour_np = np.array(contour_tuple).reshape(-1, 1, 2).astype(np.int32)

    # Create a blank image with the same shape as the original image
    blank_image = np.zeros(image_shape, dtype=np.uint8)

    # Draw the contour on the blank image
    cv2.drawContours(blank_image, [contour_np], -1, line_color, line_thickness)

    # Convert the OpenCV image to a PIL Image
    pil_image = Image.fromarray(cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB))
    
    return pil_image

def create_pdf_from_map(image_map, image_per_page = 5):
    # Define the constants
    WIDTH = 210  # A4 paper width in mm
    IMAGE_WIDTH = WIDTH * 0.4  # width for image, adjust accordingly
    MARGIN = 10  # margin in mm
    GAP = 10  # gap between image and text
    VERT_GAP = 5  # vertical gap between each image-text pair
    TEXT_HEIGHT = 10  # height of text box
    MAX_IMAGES_PER_PAGE = image_per_page

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=MARGIN)

    x_img = MARGIN
    y_img = MARGIN
    x_txt = MARGIN + IMAGE_WIDTH + GAP
    y_txt = y_img

    count = 0

    for image_tuple, value in image_map.items():
        image_data = tuple_to_pil_image(image_tuple) 

        if count == MAX_IMAGES_PER_PAGE:
            pdf.add_page()
            y_img = MARGIN
            y_txt = MARGIN
            count = 0


        if isinstance(image_data, Image.Image):
            image_stream = io.BytesIO()
            image_data.save(image_stream, format='PNG')
            image_stream.seek(0)
            img = Image.open(image_stream)
        else:
            raise ValueError("Unsupported image format")

        # Calculate aspect ratio to retain image proportions
        aspect_ratio = img.width / img.height
        image_height = IMAGE_WIDTH / aspect_ratio

        # Add image and text to PDF
        pdf.image(image_stream, x=x_img, y=y_img, w=IMAGE_WIDTH, h=image_height, type='PNG')
        pdf.set_xy(x_txt, y_txt + (image_height - TEXT_HEIGHT) / 2)  # vertically center the text
        pdf.set_font("Arial", size=12)
        pdf.cell(0, TEXT_HEIGHT, str(value))

        y_img += image_height + VERT_GAP
        y_txt = y_img
        count += 1

    pdf_output = pdf.output(dest='S').encode('latin-1')  # Convert the string output to bytes using 'latin-1' encoding
    return pdf_output
