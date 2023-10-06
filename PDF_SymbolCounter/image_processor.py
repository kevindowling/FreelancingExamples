from PIL import Image
import cv2
import numpy as np



def process_image(pil_image):
    print("processing image")
    # Convert PIL Image to OpenCV format (numpy array)
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Noise removal using Morphological operations
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Identify sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Identifying sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)


    # Identify unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add 1 to all the labels to distinguish sure regions from unknown region
    markers = markers + 1
    markers[unknown == 255] = 0

    # Apply watershed
    cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]

    # Find contours after applying watershed
    contours, _ = cv2.findContours(markers.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Tuple

    return contours

def find_contour_matches(primary_images, secondary_images, similarity_threshold=0.05):
    primary_contours = []
    secondary_contours = []
    for primary_image in primary_images:
        primary_contours.extend(process_image(primary_image))
    for secondary_image in secondary_images:
        secondary_contours.extend(process_image(secondary_image))
    
    print("Num primary contours: ", len(primary_contours))
    print("Num secondary contours: ", len(secondary_contours))
    contour_matches = {}
    primary_contour_index = 0
    secondary_contour_index = 0
    for primary_contour in primary_contours:
        primary_contour_index += 1
        print("Outerloop iteration: ", primary_contour_index)


        for secondary_contour in secondary_contours:
            secondary_contour_index += 1
            print("Innerloop iteration: ", secondary_contour_index)

    return contour_matches
            #print("Making sure the data type is correct")
            #primary_contour = primary_contour.astype(np.int32)
            #secondary_contour = secondary_contour.astype(np.int32)
"""             print("Primary contour dtype: ", primary_contour.dtype, "| Secondary contour dtype: ", secondary_contour.dtype)

           
            try:
                #similarity = cv2.matchShapes(primary_contour, secondary_contour, cv2.CONTOURS_MATCH_I1, 0)
                similarity = 0
                print("Checking primary contour (", primary_contour_index, ") with secondary contour (", secondary_contour_index, ")")
            except Exception as e:
                print("Error:", e)
                continue

            print("Checking similarity agains threshold:")
            # If the similarity is below the threshold, consider it a match
            if similarity < similarity_threshold:
                match_count += 1
                print("Matched")
            else:
                print("Not a match") """


        # Convert primary_contour to a tuple and use it as a key
        #contour_key = tuple(primary_contour.reshape(-1).tolist())
        #contour_matches[contour_key] = match_count



