import tkinter as tk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk
from tkinter import ttk

# Add your own encryption and decryption functions here
def encrypt_image(secret_message, image_path, output_path):
    pass

def decrypt_image(image_path):
    return "Hidden message"

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.create_frames()

    def create_widgets(self):
        self.encryption_button = ttk.Button(self, text="Encryption", command=self.show_encryption_frame)
        self.encryption_button.pack(side="left", padx=10, pady=10)

        self.decryption_button = ttk.Button(self, text="Decryption", command=self.show_decryption_frame)
        self.decryption_button.pack(side="left", padx=10, pady=10)

    def create_frames(self):
        self.encryption_frame = ttk.Frame(self.master)
        self.decryption_frame = ttk.Frame(self.master)

        self.encryption_widgets()
        self.decryption_widgets()

    def encryption_widgets(self):
        ttk.Label(self.encryption_frame, text="Select image:").pack(pady=5)

        self.filepath_encrypt = ttk.Entry(self.encryption_frame)
        self.filepath_encrypt.pack(pady=5)

        browse_button_encrypt = ttk.Button(self.encryption_frame, text="Browse", command=self.browse_image_encrypt)
        browse_button_encrypt.pack(pady=5)

        ttk.Label(self.encryption_frame, text="Secret Message:").pack(pady=5)

        self.secret_message = ttk.Entry(self.encryption_frame)
        self.secret_message.pack(pady=5)

        ttk.Label(self.encryption_frame, text="Output File:").pack(pady=5)

        self.output_file = ttk.Entry(self.encryption_frame)
        self.output_file.pack(pady=5)

        browse_button_output = ttk.Button(self.encryption_frame, text="Output File", command=self.browse_output_file)
        browse_button_output.pack(pady=5)

        submit_button_encrypt = ttk.Button(self.encryption_frame, text="Encrypt", command=self.encrypt)
        submit_button_encrypt.pack(pady=10)

    def decryption_widgets(self):
        ttk.Label(self.decryption_frame, text="Select image:").pack(pady=5)

        self.filepath_decrypt = ttk.Entry(self.decryption_frame)
        self.filepath_decrypt.pack(pady=5)

        browse_button_decrypt = ttk.Button(self.decryption_frame, text="Browse", command=self.browse_image_decrypt)
        browse_button_decrypt.pack(pady=5)

        submit_button_decrypt = ttk.Button(self.decryption_frame, text="Decrypt", command=self.decrypt)
        submit_button_decrypt.pack(pady=10)

    def show_encryption_frame(self):
        self.encryption_frame.pack(fill=tk.BOTH, expand=True)
        self.decryption_frame.pack_forget()

    def show_decryption_frame(self):
        self.decryption_frame.pack(fill=tk.BOTH, expand=True)
        self.encryption_frame.pack_forget()

    def browse_image_encrypt(self):
        file_path = filedialog.askopenfilename()
        self.filepath_encrypt.delete(0, tk.END)
        self.filepath_encrypt.insert(0, file_path)

    def browse_image_decrypt(self):
        file_path = filedialog.askopenfilename()
        self.filepath_decrypt.delete(0, tk.END)
        self.filepath_decrypt.insert(0, file_path)

    def browse_output_file(self):
        output_file_path = filedialog.asksaveasfilename()
        self.output_file.delete(0, tk.END)
        self.output_file.insert(0, output_file_path)


    def encrypt(self):
        image_path = self.filepath_encrypt.get()
        secret_message = self.secret_message.get()
        output_path = self.output_file.get()
        encrypt_image(secret_message, image_path, output_path)
        messagebox.showinfo("Success", "Image encrypted successfully!")

    def decrypt(self):
        image_path = self.filepath_decrypt.get()
        hidden_text = decrypt_image(image_path)
        messagebox.showinfo("Hidden Message", hidden_text)

def main():
    root = ThemedTk(theme="breeze")
    root.title("Intro to Cryptography")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()

