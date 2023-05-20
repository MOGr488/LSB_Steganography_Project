import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from ttkthemes import ThemedTk
from tkinter import ttk
from LSBSteg import LSBSteg


def encrypt_image(secret_message, image_path):
    steg = LSBSteg(cv2.imread(image_path))
    img_encoded = steg.encode_text(secret_message)
    cv2.imwrite('encrypted.png', img_encoded)


def decrypt_image(image_path):
    im = cv2.imread(image_path)
    steg = LSBSteg(im)
    return steg.decode_text()


def analyze_images(original_image_path, stegno_image_path):
    original_image = cv2.imread(original_image_path)
    stegno_image = cv2.imread(stegno_image_path)

    if original_image.shape == stegno_image.shape:
        difference = cv2.subtract(original_image, stegno_image)
        b, g, r = cv2.split(difference)

        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            messagebox.showinfo("Analysis Result", "The stego image is identical to the original image.")
        else:
            messagebox.showinfo("Analysis Result", "The stego image differs from the original image.")
    else:
        messagebox.showerror("Error", "The original and stego images have different dimensions.")


def show_encryption_frame():
    encryption_frame.pack(fill=tk.BOTH, expand=True)
    decryption_frame.pack_forget()
    analysis_frame.pack_forget()


def show_decryption_frame():
    decryption_frame.pack(fill=tk.BOTH, expand=True)
    encryption_frame.pack_forget()
    analysis_frame.pack_forget()


def show_analysis_frame():
    analysis_frame.pack(fill=tk.BOTH, expand=True)
    encryption_frame.pack_forget()
    decryption_frame.pack_forget()


def browse_image_encrypt():
    file_path = filedialog.askopenfilename()
    filepath_encrypt.delete(0, tk.END)
    filepath_encrypt.insert(0, file_path)


def browse_image_decrypt():
    file_path = filedialog.askopenfilename()
    filepath_decrypt.delete(0, tk.END)
    filepath_decrypt.insert(0, file_path)


def browse_original_image():
    file_path = filedialog.askopenfilename()
    original_image_entry.delete(0, tk.END)
    original_image_entry.insert(0, file_path)


def browse_stegno_image():
    file_path = filedialog.askopenfilename()
    stegno_image_entry.delete(0, tk.END)
    stegno_image_entry.insert(0, file_path)


def encrypt():
    image_path = filepath_encrypt.get()
    secret_message = secret_message_input.get()
    output_path = output_file.get()
    encrypt_image(secret_message, image_path)
    messagebox.showinfo("Success", "Image encrypted successfully!")


def decrypt():
    image_path = filepath_decrypt.get()
    hidden_text = decrypt_image(image_path)
    messagebox.showinfo("Hidden Message", hidden_text)


def analyze():
    original_image_path = original_image_entry.get()
    stegno_image_path = stegno_image_entry.get()
    analyze_images(original_image_path, stegno_image_path)


root = ThemedTk(theme="breeze")
root.title("Intro to Cryptography")

# Create encryption, decryption, and analysis frames
encryption_frame = ttk.Frame(root)
decryption_frame = ttk.Frame(root)
analysis_frame = ttk.Frame(root)

# Create encryption widgets
ttk.Label(encryption_frame, text="Select image:").pack(pady=5)

filepath_encrypt = ttk.Entry(encryption_frame)
filepath_encrypt.pack(pady=5, padx=10)

browse_button_encrypt = ttk.Button(encryption_frame, text="Browse", command=browse_image_encrypt)
browse_button_encrypt.pack(pady=5)

ttk.Label(encryption_frame, text="Secret Message:").pack(pady=5)

secret_message_input = ttk.Entry(encryption_frame)
secret_message_input.pack(pady=5)

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

# Create analysis widgets
ttk.Label(analysis_frame, text="Original Image:").pack(pady=5)

original_image_entry = ttk.Entry(analysis_frame)
original_image_entry.pack(pady=5, padx=10)

browse_button_original = ttk.Button(analysis_frame, text="Browse", command=browse_original_image)
browse_button_original.pack(pady=5)

ttk.Label(analysis_frame, text="Stegno Image:").pack(pady=5)

stegno_image_entry = ttk.Entry(analysis_frame)
stegno_image_entry.pack(pady=5, padx=10)

browse_button_stegno = ttk.Button(analysis_frame, text="Browse", command=browse_stegno_image)
browse_button_stegno.pack(pady=5)

submit_button_analyze = ttk.Button(analysis_frame, text="Analyze", command=analyze)
submit_button_analyze.pack(pady=10)

# Create buttons to switch between frames
encryption_button = ttk.Button(root, text="Encryption", command=show_encryption_frame)
encryption_button.pack(anchor="w", padx=10, pady=10)

decryption_button = ttk.Button(root, text="Decryption", command=show_decryption_frame)
decryption_button.pack(anchor="w", padx=10, pady=10)

analyze_button = ttk.Button(root, text="Analyze", command=show_analysis_frame)
analyze_button.pack(anchor="w", padx=10, pady=10)

root.mainloop()
