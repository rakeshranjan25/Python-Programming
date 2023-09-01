import os
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter

def browse_source_pdf():
    source_pdf_path.set(filedialog.askopenfilename())

def browse_dest_pdf():
    dest_pdf_path.set(filedialog.askopenfilename())

def browse_output_path():
    output_dir_path = filedialog.askdirectory()
    output_file_path.set(output_dir_path)

def copy_metadata():
    source_path = source_pdf_path.get()
    dest_path = dest_pdf_path.get()
    output_dir = output_file_path.get()

    try:
        source_pdf = PdfReader(source_path)
        dest_pdf = PdfReader(dest_path)

        if source_pdf.is_encrypted:
            password = input("Enter the password for the source PDF file: ")
            source_pdf.decrypt(password)

        if dest_pdf.is_encrypted:
            password = input("Enter the password for the destination PDF file: ")
            dest_pdf.decrypt(password)

        dest_pdf_info = dest_pdf.metadata

        dest_pdf_info.update({
            '/Producer': source_pdf.metadata.get('/Producer', ''),
            '/Creator': source_pdf.metadata.get('/Creator', ''),
        })

        source_create_time = source_pdf.metadata.get('/CreationDate')
        if source_create_time:
            dest_pdf_info.update({
                '/CreationDate': source_create_time
            })

        source_mod_time = source_pdf.metadata.get('/ModDate')
        if source_mod_time:
            dest_pdf_info.update({
                '/ModDate': source_mod_time
            })

        source_access_time = source_pdf.metadata.get('/AccessDate')
        if source_access_time:
            dest_pdf_info.update({
                '/AccessDate': source_access_time
            })

        source_filename = os.path.splitext(os.path.basename(source_path))[0]
        output_filename = f"{source_filename}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        output_pdf = PdfWriter()
        output_pdf.append_pages_from_reader(dest_pdf)
        output_pdf.add_metadata(dest_pdf_info)

        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)

        status_label.config(text="Metadata copied and saved successfully!")

    except Exception as e:
        status_label.config(text="Error: Failed to read PDF files.")
        print(e)

# Create the main window
root = tk.Tk()
root.title("PDF Metadata Copy Application")
root.geometry("400x400")

# Variables to store file paths
source_pdf_path = tk.StringVar()
dest_pdf_path = tk.StringVar()
output_file_path = tk.StringVar()

# Create widgets
source_label = tk.Label(root, text="Source PDF:")
source_label.pack()
source_entry = tk.Entry(root, textvariable=source_pdf_path)
source_entry.pack()
source_button = tk.Button(root, text="Browse", command=browse_source_pdf)
source_button.pack()

dest_label = tk.Label(root, text="Destination PDF:")
dest_label.pack()
dest_entry = tk.Entry(root, textvariable=dest_pdf_path)
dest_entry.pack()
dest_button = tk.Button(root, text="Browse", command=browse_dest_pdf)
dest_button.pack()

output_label = tk.Label(root, text="Output Directory:")
output_label.pack()
output_entry = tk.Entry(root, textvariable=output_file_path)
output_entry.pack()
output_button = tk.Button(root, text="Browse", command=browse_output_path)
output_button.pack()

copy_button = tk.Button(root, text="Copy Metadata", command=copy_metadata)
copy_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

# Start the main loop
root.mainloop()