import tkinter as tk
from tkinter import filedialog, messagebox
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

# Function to select PDF file to save
def select_pdf(): 
    pdf = filedialog.asksaveasfilename(
        title="Save PDF As", 
        defaultextension=".pdf", 
        initialdir="C:/", 
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
    )
    return pdf

# Main GUI setup
root = tk.Tk()
root.title("Convert Images to PDF")
root.geometry("300x100")  # Set the window size

# Buttons to select images and convert them
select_images_btn = tk.Button(root, text="Select Images", command=lambda: convert_to_pdf())
select_images_btn.pack(pady=10)

def convert_to_pdf():
    images = select_images()
    if images:
        pdf_name = select_pdf()
        if pdf_name:
            images_to_pdf(images, pdf_name)

root.mainloop()