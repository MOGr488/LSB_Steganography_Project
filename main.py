import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from ttkthemes import ThemedTk
from tkinter import ttk
from LSBSteg import LSBSteg
import matplotlib.pyplot as plt
import numpy as np


def encrypt_image(secret_message, image_path):
    steg = LSBSteg(cv2.imread(image_path))
    img_encoded = steg.encode_text(secret_message)
    cv2.imwrite('encrypted.png', img_encoded)


def decrypt_image(image_path):
    im = cv2.imread(image_path)
    steg = LSBSteg(im)
    return steg.decode_text()


def analyze_images_heatmap():
    original_image_path = original_image_entry.get()
    stegno_image_path = stegno_image_entry.get()
    original_image = cv2.imread(original_image_path)
    stegno_image = cv2.imread(stegno_image_path)

    if original_image.shape == stegno_image.shape:
        difference = cv2.subtract(original_image, stegno_image)
        difference_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

        if cv2.countNonZero(difference_gray) == 0:
            messagebox.showinfo("Analysis Result", "The stego image is identical to the original image.")
        else:
            messagebox.showinfo("Analysis Result", "The stego image differs from the original image.")

            # Display the difference heatmap using matplotlib
            fig, ax = plt.subplots(figsize=(8, 8))
            heatmap = ax.imshow(difference_gray, cmap='hot')
            plt.colorbar(heatmap)

            plt.title("Difference Heatmap")
            plt.axis('off')
            plt.show()
    else:
        messagebox.showerror("Error", "The original and stego images have different dimensions.")


def calc_histogram(image):
    hist = np.zeros((256, 3), dtype=np.float32)
    for i in range(3):
        hist[:, i] = cv2.calcHist([image], [i], None, [256], [0, 256]).flatten()  # Flatten the histogram array
    return hist


def get_channel_color(channel):
    colors = ['red', 'green', 'blue']
    return colors[channel]


def get_channel_name(channel):
    names = ['Red Channel', 'Green Channel', 'Blue Channel']
    return names[channel]


def plot_histogram_difference(original_hist, stegno_hist):
    diff_hist = np.abs(original_hist - stegno_hist)

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
    titles = ['Red Channel', 'Green Channel', 'Blue Channel']

    for i in range(2):
        for j in range(3):
            axes[i, j].bar(np.arange(256), diff_hist[:, j], color=get_channel_color(j))
            axes[i, j].set_xlim([0, 256])
            axes[i, j].set_title(titles[j])
            axes[i, j].set_xlabel('Pixel Intensity')
            axes[i, j].set_ylabel('Absolute Difference')

    plt.tight_layout()
    plt.show()


def analyze_images(original_image_path, stegno_image_path):
    original_image = cv2.imread(original_image_path)
    stegno_image = cv2.imread(stegno_image_path)

    if original_image.shape == stegno_image.shape:
        # Calculate histograms for original image and stego image
        original_hist = calc_histogram(original_image)
        stegno_hist = calc_histogram(stegno_image)

        # Display images and histograms using matplotlib
        fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 8))
        titles = ['Original Image', 'Stego Image']
        images = [original_image, stegno_image]
        hist_data = [original_hist, stegno_hist]

        for i in range(2):
            # Display the image
            axes[i, 0].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
            axes[i, 0].set_title(titles[i])
            axes[i, 0].axis('off')

            # Display the histograms
            for j in range(3):
                axes[i, j + 1].plot(hist_data[i][:, j], color=get_channel_color(j))
                axes[i, j + 1].set_xlim([0, 256])
                axes[i, j + 1].set_title(get_channel_name(j))

        # Calculate and display the difference histograms
        diff_hist_title = 'Histogram Difference'
        plot_histogram_difference(original_hist, stegno_hist)

        # Remove unused subplots in the third row
        for j in range(3):
            axes[1, j + 1].remove()


    else:
        messagebox.showerror("Error", "The original and stego images have different dimensions.")


def show_encryption_frame():
    encryption_frame.grid(row=0, column=1, sticky="nsew")
    decryption_frame.grid_remove()
    analysis_frame.grid_remove()


def show_decryption_frame():
    decryption_frame.grid(row=0, column=1, sticky="nsew")
    encryption_frame.grid_remove()
    analysis_frame.grid_remove()


def show_analysis_frame():
    analysis_frame.grid(row=0, column=1, sticky="nsew")
    encryption_frame.grid_remove()
    decryption_frame.grid_remove()


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
root.geometry("310x360")

# Create encryption, decryption, and analysis label frames
encryption_frame = ttk.LabelFrame(root, text="Encryption")
decryption_frame = ttk.LabelFrame(root, text="Decryption")
analysis_frame = ttk.LabelFrame(root, text="Analysis")

# Set grid configurations for root and frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

encryption_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
decryption_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
analysis_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Create encryption widgets
ttk.Label(encryption_frame, text="Select image:").grid(row=0, column=0, pady=5)

filepath_encrypt = ttk.Entry(encryption_frame)
filepath_encrypt.grid(row=1, column=0, pady=5, padx=10)

browse_button_encrypt = ttk.Button(encryption_frame, text="Browse", command=browse_image_encrypt)
browse_button_encrypt.grid(row=2, column=0, pady=5)

ttk.Label(encryption_frame, text="Secret Message:").grid(row=3, column=0, pady=5)

secret_message_input = ttk.Entry(encryption_frame)
secret_message_input.grid(row=4, column=0, pady=5)

submit_button_encrypt = ttk.Button(encryption_frame, text="Encrypt", command=encrypt)
submit_button_encrypt.grid(row=5, column=0, pady=10)

# Create decryption widgets
ttk.Label(decryption_frame, text="Select image:").grid(row=0, column=0, pady=5)

filepath_decrypt = ttk.Entry(decryption_frame)
filepath_decrypt.grid(row=1, column=0, pady=5, padx=10)

browse_button_decrypt = ttk.Button(decryption_frame, text="Browse", command=browse_image_decrypt)
browse_button_decrypt.grid(row=2, column=0, pady=5)

submit_button_decrypt = ttk.Button(decryption_frame, text="Decrypt", command=decrypt)
submit_button_decrypt.grid(row=3, column=0, pady=10)

# Create analysis widgets
ttk.Label(analysis_frame, text="Original Image:").grid(row=0, column=0, pady=5)

original_image_entry = ttk.Entry(analysis_frame)
original_image_entry.grid(row=1, column=0, pady=5, padx=10)

browse_button_original = ttk.Button(analysis_frame, text="Browse", command=browse_original_image)
browse_button_original.grid(row=2, column=0, pady=5)

ttk.Label(analysis_frame, text="Stegno Image:").grid(row=3, column=0, pady=5)

stegno_image_entry = ttk.Entry(analysis_frame)
stegno_image_entry.grid(row=4, column=0, pady=5, padx=10)

browse_button_stegno = ttk.Button(analysis_frame, text="Browse", command=browse_stegno_image)
browse_button_stegno.grid(row=5, column=0, pady=5)

submit_button_analyze = ttk.Button(analysis_frame, text=" \U0001F4CA Analyze", command=analyze)
submit_button_analyze.grid(row=6, column=0, pady=20)

submit_button_heatmap = ttk.Button(analysis_frame, text="🌡 Heatmap", command=analyze_images_heatmap)
submit_button_heatmap.grid(row=7, column=0, pady=7)

# Create main buttons frame
main_buttons_frame = ttk.LabelFrame(root, text="Main Buttons")
main_buttons_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

# Create buttons to switch between frames
encryption_button = ttk.Button(main_buttons_frame, text="Encryption", command=show_encryption_frame)
encryption_button.pack(padx=10, pady=10, fill=tk.X)

decryption_button = ttk.Button(main_buttons_frame, text="Decryption", command=show_decryption_frame)
decryption_button.pack(padx=10, pady=10, fill=tk.X)

analyze_button = ttk.Button(main_buttons_frame, text="Analyze", command=show_analysis_frame)
analyze_button.pack(padx=10, pady=10, fill=tk.X)

root.mainloop()
