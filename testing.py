import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from ttkthemes import ThemedTk
from tkinter import ttk
from LSBSteg import LSBSteg

# Add your own encryption and decryption functions here
def encrypt_image(secret_message, image_path, output_path):
    steg = LSBSteg(cv2.imread(image_path))
    img_encoded = steg.encode_text(secret_message)
    cv2.imwrite(output_path, img_encoded)


def decrypt_image(image_path):
    return "Hidden message"


def show_encryption_frame():
    encryption_frame.pack(fill=tk.BOTH, expand=True)
    decryption_frame.pack_forget()


def show_decryption_frame():
    decryption_frame.pack(fill=tk.BOTH, expand=True)
    encryption_frame.pack_forget()


def browse_image_encrypt():
    file_path = filedialog.askopenfilename()
    filepath_encrypt.delete(0, tk.END)
    filepath_encrypt.insert(0, file_path)


def browse_image_decrypt():
    file_path = filedialog.askopenfilename()
    filepath_decrypt.delete(0, tk.END)
    filepath_decrypt.insert(0, file_path)


def browse_output_file():
    output_file_path = filedialog.asksaveasfilename()
    output_file.delete(0, tk.END)
    output_file.insert(0, output_file_path)


def encrypt():
    image_path = filepath_encrypt.get()
    secret_message = secret_message_input.get()
    output_path = output_file.get()
    encrypt_image(secret_message, image_path, output_path)
    messagebox.showinfo("Success", "Image encrypted successfully!")


def decrypt():
    image_path = filepath_decrypt.get()
    hidden_text = decrypt_image(image_path)
    messagebox.showinfo("Hidden Message", hidden_text)


root = ThemedTk(theme="breeze")
root.title("Intro to Cryptography")

# Create encryption and decryption frames
encryption_frame = ttk.Frame(root)
decryption_frame = ttk.Frame(root)

# Create encryption widgets
ttk.Label(encryption_frame, text="Select image:").pack(pady=5)

filepath_encrypt = ttk.Entry(encryption_frame)
filepath_encrypt.pack(pady=5, padx=10)

browse_button_encrypt = ttk.Button(encryption_frame, text="Browse", command=browse_image_encrypt)
browse_button_encrypt.pack(pady=5)

ttk.Label(encryption_frame, text="Secret Message:").pack(pady=5)

secret_message_input = ttk.Entry(encryption_frame)
secret_message_input.pack(pady=5)

ttk.Label(encryption_frame, text="Output File:").pack(pady=5)

output_file = ttk.Entry(encryption_frame)
output_file.pack(pady=5)

browse_button_output = ttk.Button(encryption_frame, text="Output File", command=browse_output_file)
browse_button_output.pack(pady=5)

submit_button_encrypt = ttk.Button(encryption_frame, text="Encrypt", command=encrypt)
submit_button_encrypt.pack(pady=10)

# Create decryption widgets
ttk.Label(decryption_frame, text="Select image:").pack(pady=5)

filepath_decrypt = ttk.Entry(decryption_frame)
filepath_decrypt.pack(pady=5, padx=10)

browse_button_decrypt = ttk.Button(decryption_frame, text="Browse", command=browse_image_decrypt)
browse_button_decrypt.pack(pady=5)

submit_button_decrypt = ttk.Button(decryption_frame, text="Decrypt", command=decrypt)
submit_button_decrypt.pack(pady=10)

# Create buttons to switch between frames
encryption_button = ttk.Button(root, text="Encryption", command=show_encryption_frame)
encryption_button.pack(side="left", padx=10, pady=10)

decryption_button = ttk.Button(root, text="Decryption", command=show_decryption_frame)
decryption_button.pack(side="left", padx=10, pady=10)

root.mainloop()
