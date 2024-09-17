import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import zipfile
import os

# Function to convert a single image to PDF and return the PDF filename
def image_to_pdf(image_path, pdf_name):
    try:
        img = Image.open(image_path)
        if img.mode in ("RGBA", "P"):  
            img = img.convert("RGB")
        img.save(pdf_name, "PDF", resolution=100.0)
        return pdf_name
    except Exception as e:
        messagebox.showerror("Error", f"Ошибка при конвертации изображения в PDF.\nError: {str(e)}")
        return None

# Function to select images
def select_images():
    images = filedialog.askopenfilenames(
        title="Выберите изображения", 
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")), 
        initialdir="C:/"
    )
    return images

# Function to select directory to save ZIP
def select_directory(): 
    directory = filedialog.askdirectory(
        title="Выберите папку для сохранения ZIP", 
        initialdir="C:/"
    )
    return directory

# Function to get the full path for saving ZIP
def get_zip_path():
    directory = select_directory()
    if directory:
        zip_name = filedialog.asksaveasfilename(
            title="Сохранить ZIP как", 
            defaultextension=".zip", 
            initialdir=directory, 
            filetypes=(("ZIP files", "*.zip"), ("All files", "*.*")),
            initialfile="output.zip"
        )
        return zip_name
    return None

# Function to convert images to PDFs and archive them in a ZIP file
def images_to_zip(images, zip_name):
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for image_path in images:
                # Generate PDF name for each image
                pdf_name = os.path.splitext(os.path.basename(image_path))[0] + ".pdf"
                # Convert the image to a PDF
                pdf_path = image_to_pdf(image_path, pdf_name)
                if pdf_path:
                    # Add the PDF to the ZIP archive
                    zipf.write(pdf_path, os.path.basename(pdf_path))
                    # Remove the temporary PDF file after adding it to ZIP
                    os.remove(pdf_path)
        messagebox.showinfo("Success", "Изображения успешно конвертированы и заархивированы в ZIP.")
    except Exception as e:
        messagebox.showerror("Error", f"Ошибка при создании ZIP архива.\nError: {str(e)}")

# Function to update the file list on the GUI
def update_file_list(file_list_frame, inner_frame, selected_images):
    # Clear the current list
    for widget in inner_frame.winfo_children():
        widget.destroy()

    if selected_images:
        for i, image in enumerate(selected_images):
            image_name = os.path.basename(image)

            # Create a frame for each image with its name and remove button
            image_frame = tk.Frame(inner_frame, bg="#f0f0f0", pady=2)

            # Image name label
            file_label = tk.Label(image_frame, text=f"{i + 1}. {image_name}", font=("Helvetica", 10), bg="#f0f0f0")
            file_label.pack(side=tk.LEFT, padx=5)

            # Remove button
            remove_btn = tk.Button(image_frame, text="Удалить", command=lambda idx=i: remove_image(idx), font=("Helvetica", 10), bg="#dc3545", fg="white", relief=tk.RAISED, padx=5, pady=2)
            remove_btn.pack(side=tk.RIGHT)

            # Pack the frame into the canvas window
            image_frame.pack(fill=tk.X)

        # Update scroll region
        file_list_frame.update_idletasks()
        file_list_frame.config(scrollregion=file_list_frame.bbox("all"))

# Main GUI setup
root = tk.Tk()
root.title("GR1175 Convertor")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

# Frame for better layout control
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Title label
title_label = tk.Label(frame, text="Конвертер изображений", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=(10, 5))

# Instructions label
instructions_label = tk.Label(frame, text="Выберите изображения для конвертации.", font=("Helvetica", 12), bg="#f0f0f0")
instructions_label.pack(pady=(0, 20))

# Variable to store selected images
selected_images = []

# Button to select images
select_images_btn = tk.Button(frame, text="Добавить изображения", command=lambda: add_images(), font=("Helvetica", 12), bg="#007bff", fg="white", relief=tk.RAISED, padx=10, pady=5)
select_images_btn.pack(pady=10)

# Scrollable area to display selected files
scrollable_frame = tk.Frame(frame)
scrollable_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Create a canvas to hold the file list with scrollbar
file_list_canvas = tk.Canvas(scrollable_frame, height=150, bg="#f0f0f0")
file_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the file list
scrollbar = tk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=file_list_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure canvas scroll
file_list_canvas.config(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the file entries
inner_frame = tk.Frame(file_list_canvas, bg="#f0f0f0")
file_list_frame = file_list_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Bind mouse wheel to scroll
file_list_canvas.bind("<Configure>", lambda e: file_list_canvas.config(scrollregion=file_list_canvas.bbox("all")))

# Button to convert images to ZIP (disabled by default)
convert_btn = tk.Button(frame, text="Конвертировать в PDF", state=tk.DISABLED, command=lambda: convert_to_zip(), font=("Helvetica", 12), bg="#28a745", fg="white", relief=tk.RAISED, padx=10, pady=5)
convert_btn.pack(pady=10)

# Function to handle adding images
def add_images():
    global selected_images
    images = select_images()
    if images:
        selected_images.extend(list(images))  
        update_file_list(file_list_canvas, inner_frame, selected_images)  
        convert_btn.config(state=tk.NORMAL) 

# Function to remove an image by index
def remove_image(index):
    global selected_images
    if 0 <= index < len(selected_images):
        del selected_images[index] 
        update_file_list(file_list_canvas, inner_frame, selected_images) 
        if not selected_images:
            convert_btn.config(state=tk.DISABLED)  

# Function to handle conversion
def convert_to_zip():
    if selected_images:
        zip_name = get_zip_path()
        if zip_name:
            images_to_zip(selected_images, zip_name)

root.mainloop()
