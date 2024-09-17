import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

# Function to convert images to PDF
def images_to_pdf(images, pdf_name):
    try:
        # Create new PDF file from the first image
        pdf = Image.open(images[0])
        pdf.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
        
        messagebox.showinfo("Success", "Images have been successfully converted to PDF.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert images to PDF.\nError: {str(e)}")

# Function to select images
def select_images():
    images = filedialog.askopenfilenames(
        title="Select Images", 
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")), 
        initialdir="C:/"
    )
    return images

# Function to select directory to save PDF
def select_directory(): 
    directory = filedialog.askdirectory(
        title="Select Directory", 
        initialdir="C:/"
    )
    return directory

# Function to get the full path for saving PDF
def get_pdf_path():
    directory = select_directory()
    if directory:
        pdf_name = filedialog.asksaveasfilename(
            title="Save PDF As", 
            defaultextension=".pdf", 
            initialdir=directory, 
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")),
            initialfile="output.pdf"
        )
        return pdf_name
    return None

# Main GUI setup
root = tk.Tk()
root.title("Convert Images to PDF")
root.geometry("400x200")  # Set the window size
root.configure(bg="#f0f0f0")  # Background color

# Frame for better layout control
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Title label
title_label = tk.Label(frame, text="Image to PDF Converter", font=("Helvetica", 16), bg="#f0f0f0")
title_label.pack(pady=10)

# Buttons to select images and convert them
select_images_btn = tk.Button(frame, text="Select Images", command=lambda: convert_to_pdf(), font=("Helvetica", 12), bg="#007bff", fg="white", relief=tk.RAISED)
select_images_btn.pack(pady=10)

# Instructions label
instructions_label = tk.Label(frame, text="Click the button to select images and convert them to a PDF.", font=("Helvetica", 10), bg="#f0f0f0")
instructions_label.pack(pady=5)

def convert_to_pdf():
    images = select_images()
    if images:
        pdf_name = get_pdf_path()
        if pdf_name:
            images_to_pdf(images, pdf_name)

root.mainloop()
