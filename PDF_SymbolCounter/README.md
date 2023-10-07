
# PDF Shape Matcher Project

---

## Objective:

The primary objective of this program is to identify all instances where shapes/symbols in the first PDF document are found in the second PDF document. It aims to provide an automated way to match and compare symbols between two PDFs.

---

## GUI Preview:

![GUI Preview](https://github.com/kevindowling/FreelancingExamples/blob/main/PDF_SymbolCounter/GUI.PNG)

---

## Description:

The PDF Shape Matcher is a project designed to process PDF files, extract symbols/shapes from them, and compare and match these shapes. The GUI provides an interactive way to drag-and-drop PDF files, process them, and download the resultant PDF with matched symbols.

---

## Features:

1. **GUI**:
   - Drag-and-drop support for adding PDF files.
   - Limitation to adding only two PDF files at a time.
   - Button to process the PDFs and another to download the processed file.

2. **Image Processing**:
   - Extraction of unique symbols from the provided images.
   - Clustering of similar symbols based on histogram comparison.
   - Contour extraction from images.
  
3. **PDF Processing**:
   - Conversion of PDF files into image lists.
   - Generation of a new PDF from a map of images.

---

## Limitations/Unfinished Features:

1. There are complications where shapes are found multiple times.
2. The comparison mechanism between two shapes is not yet implemented.
3. There's ongoing work on how to detect overlapping shapes.

---

## Dependencies:

1. `tkinter` and `tkinterdnd2` for the GUI.
2. `pdf2image` for converting PDF pages to images.
3. `fpdf` for generating PDFs.
4. `PIL`, `cv2`, `numpy`, `matplotlib`, and `sklearn` for image processing tasks.

---

## How to Use:

1. Launch the GUI.
2. Drag and drop two PDF files onto the designated area.
3. Click the "Process" button.
4. Once processed, click the "Download" button to save the resultant PDF.

---

## Note:

This project is currently in development. Feedback and contributions are welcome.

