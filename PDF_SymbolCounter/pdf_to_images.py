from pdf2image import convert_from_path

def pdf_to_image_list(pdf_path):
    # Convert PDF to list of images
    images = convert_from_path(pdf_path)
    return images

