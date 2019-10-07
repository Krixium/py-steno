from tkinter import *
from tkinter import ttk, filedialog

from PIL import ImageTk, Image

from dcutils import generate_key, save_bytes_to_file, get_raw_bytes_from_file
from dcstego import steno_image, unsteno_image
from dcimage import get_bytes_from_image, save_bytes_to_image, get_image_size

import io


# Helper method for updating widgets
def open_file_and_update_label(string: StringVar, label: ttk.Label):
    string.set(filedialog.askopenfilename())
    label["textvariable"] = string


def convert_image_to_byte_array(filename: str) -> bytes:
    # Opens the secret image and converts it into bytes format
    img = Image.open(filename)
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format=img.format)
    return img_byte_array.getvalue()


def load_key_file(key_fname: StringVar, key_label: ttk.Label):
    key_fname.set(filedialog.askopenfilename())
    key_in_byte_format = get_raw_bytes_from_file(key_fname.get())
    key_string = "".join(map(chr, key_in_byte_format))
    key_fname.set(key_string)
    key_label["textvariable"] = key_fname
    return key_in_byte_format


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        self.left_frame = ttk.LabelFrame(master, text="Encrypt")
        self.left_frame.grid(column=0, row=0, sticky=N)

        self.right_frame = ttk.LabelFrame(master, text="Decrypt")
        self.right_frame.grid(column=1, row=0, sticky=N)

        self.decrypt_key_fname = StringVar()
        self.decrypt_key_file_label = ttk.Label(self.right_frame, textvariable=self.decrypt_key_fname)
        self.decrypt_key_file_label.pack()
        self.choose_decrypt_key_btn = ttk.Button(self.right_frame, text="Load decryption key file",
                                                 command=self.load_decryption_key_file)
        self.choose_decrypt_key_btn.pack()

        self.hidden_fname = StringVar()
        self.hidden_label = ttk.Label(self.right_frame, textvariable=self.hidden_fname)
        self.hidden_label.pack()
        self.choose_secret_img = ttk.Button(self.right_frame, text="Choose an image that contains a secret")
        self.choose_secret_img["command"] = self.load_hidden_file
        self.choose_secret_img.pack()

        self.extract_btn = ttk.Button(self.right_frame, text="Extract secret", command=self.unsteno_image)
        self.extract_btn.pack()

        # Defining class members related to key generation
        self.encryption_key = 1
        self.decryption_key = 1

        self.encrypt_key_fname = StringVar()
        self.encrypt_key_fname.set("keyfile")
        self.encrypt_key_label = ttk.Label(self.left_frame, textvariable=self.encrypt_key_fname)
        self.encrypt_key_label.pack()
        self.encrypt_key_label["textvariable"] = self.encrypt_key_fname
        self.choose_encrypt_key_button = ttk.Button(self.left_frame, text="Load encryption key file",
                                                    command=self.load_encryption_key_file)
        self.choose_encrypt_key_button.pack()

        # Defining class members related to the carrier image
        self.carrier_fname = StringVar()
        self.carrier_label = ttk.Label(self.left_frame, textvariable=self.carrier_fname)
        self.carrier_label.pack()
        self.carrier_image_button = ttk.Button(self.left_frame, text="Choose carrier image",
                                               command=self.load_carrier_file)
        self.carrier_image_button.pack()

        # Class members related to the secret image
        self.secret_fname = StringVar()
        self.secret_label = ttk.Label(self.left_frame, textvariable=self.secret_fname)
        self.secret_label.pack()
        self.secret_image_button = ttk.Button(self.left_frame, text="Choose secret to hide",
                                              command=self.load_secret_file)
        self.secret_image_button.pack()

        self.stego_img_fname = StringVar()
        self.stego_img_fname.set("Enter save filename here")
        self.stego_button = ttk.Button(self.left_frame, text="Hide secret image in carrier image",
                                       command=self.steno_image)
        self.stego_button.pack()

    def load_carrier_file(self):
        open_file_and_update_label(self.carrier_fname, self.carrier_label)

    def load_secret_file(self):
        open_file_and_update_label(self.secret_fname, self.secret_label)

    def load_hidden_file(self):
        open_file_and_update_label(self.hidden_fname, self.hidden_label)

    def load_encryption_key_file(self):
        self.encryption_key = load_key_file(self.encrypt_key_fname, self.encrypt_key_label)

    def load_decryption_key_file(self):
        self.decryption_key = load_key_file(self.decrypt_key_fname, self.decrypt_key_file_label)

    def generate_key(self):
        self.encryption_key = generate_key(16)
        key_string = "".join(map(chr, self.encryption_key))
        self.encrypt_key_fname.set(key_string)
        self.encrypt_key_label["textvariable"] = self.encrypt_key_fname

    def steno_image(self):
        img_byte_array = get_raw_bytes_from_file(self.secret_fname.get())
        stenod_image = steno_image(self.encryption_key, img_byte_array, self.carrier_fname.get())
        options = {'defaultextension': ".bmp", 'filetypes': [("PNG files", ".png"), ("BMP files", ".bmp")],
                   'title': "Save carrier image embedded with secret as"}
        stenod_img_filename = filedialog.asksaveasfilename(**options)
        width, height = get_image_size(self.carrier_fname.get())
        save_bytes_to_image(stenod_image, stenod_img_filename, width, height)

    def unsteno_image(self):
        hidden = self.hidden_fname.get()
        extracted_secret = unsteno_image(self.decryption_key, hidden)
        options = {'filetypes': [("PNG files", "*.png"), ("All files", "*.*")],
                   'title': "Save extracted secret as"}
        extracted_secret_file = filedialog.asksaveasfilename(**options)
        save_bytes_to_file(extracted_secret_file, extracted_secret)


if __name__ == '__main__':
    root = Tk()
    root.title("Steganography")
    root.minsize(200, 200)
    app = Application(master=root)
    app.mainloop()
