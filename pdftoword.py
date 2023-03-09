import tkinter as tk
from tkinter import filedialog, ttk
import os
import pdf2docx

pdftoword = tk.Tk()
pdftoword.geometry("450x600")
pdftoword.title("PDF to Word Converter")
pdftoword.resizable(False,False)

# Set custom styles for the widgets
style = ttk.Style(pdftoword)

style.configure("TButton", foreground="black", font=("Arial", 12, "bold"), background="#353535")
style.map("TButton", foreground=[("active", "white")], background=[("active", "#353535")])
style.configure("TLabel", font=("Arial", 12), foreground="white", background="#353535")
pdftoword.config(bg="#353535")
style.configure("TEntry", font=("Arial", 12), borderwidth=2, relief=tk.GROOVE, foreground="white", background="#353535")

# Function to convert PDF file to Word document
def convert_pdf_to_docx():
    file_path = path_entry.get()
    if not file_path:
        status_label.config(text="No file selected.")
    else:
        # Convert selected file to Word document
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        docx_file = file_name + ".docx"
        pdf2docx.parse(file_path, docx_file)
        # Enable "Open Folder" button
        open_folder_button.config(state="normal")
        # Save the path of the converted Word document
        global docx_path
        docx_path = os.path.join(os.path.dirname(file_path), docx_file)

# Function to open file dialog and select PDF file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    path_entry.delete(0, tk.END)
    path_entry.insert(0, file_path)
    # Disable "Open Folder" button
    open_folder_button.config(state="disabled")

# Function to open the folder where the converted Word document is saved
def open_folder():
    os.startfile(os.path.dirname(docx_path))

# Create label and entry for file path
path_label = ttk.Label(pdftoword, text="PDF file path:")
path_label.pack(side=tk.TOP, padx=5, pady=5)

path_entry = ttk.Entry(pdftoword, width=50)
path_entry.pack(side=tk.TOP, padx=5, pady=5)

# Create buttons to browse for file and convert PDF to Word
button_frame = tk.Frame(pdftoword, background="#353535")
button_frame.pack(side=tk.TOP, padx=5, pady=5)

browse_button = ttk.Button(button_frame, text="Browse", command=browse_file, style="TButton")
browse_button.pack(side=tk.LEFT, padx=5, pady=5)

convert_button = ttk.Button(button_frame, text="Convert", command=convert_pdf_to_docx, style="TButton")
convert_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create button to open the folder where the converted Word document is saved
open_folder_button = ttk.Button(pdftoword, text="Open Folder", command=open_folder, style="TButton", state="disabled")
open_folder_button.pack(padx=5, pady=5)

# Create label and progress bar for status
status_label = ttk.Label(pdftoword, text="", style="TLabel")
status_label.pack(side=tk.BOTTOM, padx=5, pady=5)

pdftoword.mainloop()
