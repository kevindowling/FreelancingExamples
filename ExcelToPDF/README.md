# Excel to PDF Converter Guide

This guide explains how a program reads information from an Excel sheet and creates individual PDF files with that information.

## Overview
- **What it does**: The program reads each row of information from an Excel sheet and creates a separate PDF file for each row.
- **Libraries Used**: The program uses special tools (libraries) to read Excel files and create PDF files. These are `openpyxl` for Excel files and `reportlab` for PDF files.

## How it Works
1. **Opening the Excel File**: The program opens the Excel file and looks at the active sheet (the sheet that is open when the file is opened).
2. **Reading Each Row**: The program reads the information from each row, starting from the second row (it assumes the first row has the column names).
3. **Extracting Information**: For each row, the program gets the customer name, address, service name, and date of service.
4. **Formatting Address and Date**: The program adjusts the address to only include the street and adjusts the date to the 'M/D/Y' format.
5. **Creating PDFs**: The program creates a new PDF file for each row and writes a thank-you message to the customer using the extracted information.
6. **Saving PDFs**: Finally, the program saves each PDF file with the customer's name as part of the file name.

## Steps to Run the Program
1. **Install Necessary Tools**: Before running the program, special tools (libraries) need to be installed. This can be done by someone who knows how to run commands on the computer.
2. **Provide Excel File**: The Excel file's location needs to be specified in the program.
3. **Run the Program**: Once the above steps are done, the program can be run to create the PDF files.

## Note
- This program needs to be set up and run by someone with a basic understanding of running Python scripts, but once it's set up, it can run automatically without needing any coding knowledge.
