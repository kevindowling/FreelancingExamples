import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# Load the workbook and select the active sheet
workbook = openpyxl.load_workbook('CustomerSheet.xlsx')
sheet = workbook.active

def format_address(address):
    # Assuming the address is in the format: "Street, City, State, Zip"
    # Split by comma and take only the first part (Street)
    # Adjust as needed based on your actual address format
    return address.split(',')[0].strip()

def format_date(date_of_service):
    # Assuming date_of_service is a datetime object
    # If it's a string, you may need to parse it first using datetime.strptime
    return date_of_service.strftime('%m/%d/%Y')

# Loop through the rows in the sheet starting from the second row
for row in sheet.iter_rows(min_row=2, values_only=True):
    customer_name, address, phone_number, email, service_name, cost_of_service, date_of_service = row
    
    # Format address and date
    address = format_address(address)
    date_of_service = format_date(date_of_service)
    
    # Create a new PDF file for each row
    c = canvas.Canvas(f"{customer_name}_invoice.pdf", pagesize=letter)
    width, height = letter
    
    # Write the content to the PDF
    c.drawString(100, 750, f"Dear {customer_name},")
    c.drawString(100, 730, f"Thank you for ordering {service_name} at {address} on {date_of_service}.")
    c.drawString(100, 710, "We appreciate your business. Please feel free to contact us by email or phone.")
    c.drawString(100, 690, "Sincerely,")
    c.drawString(100, 670, "Kevin Dowling")
    
    # Save the PDF
    c.save()

print("PDFs have been created successfully.")
