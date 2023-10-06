import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import image_processor as ip
import pdf_to_images as p2i
import images_to_pdf as i2p

global symbol_matches_map

def on_drop(event):
    # Get the current list of files
    current_files = list(pdf_listbox.get(0, tk.END))
    
    # If there are already 2 files, show an error
    if len(current_files) >= 2:
        messagebox.showerror("Error", "Only 2 PDFs can be added!")
        return
    
    # Get the dropped file path
    dropped_file = event.data.strip()
    
    # Check if the file is a PDF
    if not dropped_file.lower().endswith(".pdf"):
        messagebox.showerror("Error", "Only PDF files are accepted!")
        return

    pdf_listbox.insert(tk.END, dropped_file)

def process_pdfs():
    pdfs_to_process = pdf_listbox.get(0,tk.END)

    if len(pdfs_to_process) != 2:
        messagebox.showerror("Error", "Please drop exactly 2 PDFs!")
        return
    
    pdf1_images = p2i.pdf_to_image_list(pdfs_to_process[0])
    pdf2_images = p2i.pdf_to_image_list(pdfs_to_process[1])

    global symbol_matches_map
    symbol_matches_map = ip.find_contour_matches(pdf1_images,pdf2_images, 0.5) #This assumes that all symbols from first file are unique

    pass

def download_processed_file():
    global symbol_matches_map
    if(len(symbol_matches_map) > 0):
        
      pdf_output =  i2p.create_pdf_from_map()

    target_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    
    if not target_file:
        return  # The user canceled the dialog
    
    try:
        with open(target_file, 'wb') as f:
            f.write(pdf_output)
        messagebox.showinfo("Success", "File has been saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    pass

#----------------------------------------------------------------------------------------------#


root = TkinterDnD.Tk()
root.title('PDF Processor')
root.geometry('300x400')

# Drop PDF files section
label = tk.Label(root, text='Drop your PDFs here:')
label.pack(pady=20)

pdf_listbox = tk.Listbox(root, width=40, height=4)
pdf_listbox.pack(pady=20)
pdf_listbox.drop_target_register(DND_FILES)
pdf_listbox.dnd_bind('<<Drop>>', on_drop)

# Process button
process_button = tk.Button(root, text='Process', command=process_pdfs)
process_button.pack(pady=20)

# Download button
download_button = tk.Button(root, text='Download', command=download_processed_file)
download_button.pack(pady=20)

root.mainloop()
