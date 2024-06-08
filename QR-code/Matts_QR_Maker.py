# --------------------------------------------------------------------------------
# Copyright (c) 2023 Matthew Albright
# 
# This software is the intellectual property of the author, and can not be 
# distributed, used, copied, or modified without explicit permission from the author.
# --------------------------------------------------------------------------------


import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import io
import win32clipboard
from PIL import Image

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def generate_qr():
    # Get URL from the text entry
    url = url_entry.get()
    if url.strip() == "":
        messagebox.showerror("Error", "Please enter a valid URL")
        return
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    global img
    img = qr.make_image(fill='black', back_color='white')

    # Convert PIL image to ImageTk format
    img_tk = ImageTk.PhotoImage(image=img)
    qr_label.img_tk = img_tk  # Keep a reference!
    qr_label.config(image=img_tk)
    qr_label.image = img_tk  # Keep another reference!

def save_qr():
    # Open file dialog to save the image
    file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                             filetypes=[("PNG files", '*.png'), ("All files", '*.*')])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Save", "QR code saved successfully!")

def copy_to_clipboard(event):
    # Convert the PIL image 'img' to a DIB for clipboard
    output = io.BytesIO()
    img.save(output, format="BMP")
    data = output.getvalue()[14:]  # BMP file header length is 14 bytes
    output.close()
    
    send_to_clipboard(win32clipboard.CF_DIB, data)
    messagebox.showinfo("Clipboard", "Image copied to clipboard.")

# Set up the main application window
root = tk.Tk()
root.title("QR Code Generator")

# Create a label to prompt for URL
label = tk.Label(root, text="Enter URL:")
label.pack(pady=(10,0))

# Create a text entry widget for inputting the URL
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=10)

# Create a button to generate QR code
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=(0,10))

# Create a label to display the QR code
qr_label = tk.Label(root)
qr_label.pack(pady=10)
qr_label.bind("<Button-3>", copy_to_clipboard)  # Bind right-click to copy function

# Create a save button to save the QR code
save_button = tk.Button(root, text="Save QR Code", command=save_qr)
save_button.pack(pady=(0,10))

# Start the GUI event loop
root.mainloop()
