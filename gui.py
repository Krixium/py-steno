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
        self.choose_decrypt_key_btn = ttk.Button(self.right_frame, text="Load decryption key file", command=self.load_decryption_key_file)
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

        self.encrypt_key_fname = StringVar()
        self.encrypt_key_fname.set("Key not loaded")
        self.encrypt_key_label = ttk.Label(self.left_frame, textvariable=self.encrypt_key_fname)
        self.encrypt_key_label.pack()
        self.encrypt_key_label["textvariable"] = self.encrypt_key_fname
        self.choose_encrypt_key_button = ttk.Button(self.left_frame, text="Load encryption key file", command=self.load_encryption_key_file)
        self.choose_encrypt_key_button.pack()

        # Defining class members related to the carrier image
        self.carrier_fname = StringVar()
        self.carrier_fname.set("images/jojo_meme_001.png")
        self.carrier_label = ttk.Label(self.left_frame, textvariable=self.carrier_fname)
        self.carrier_label.pack()
        self.carrier_image_button = ttk.Button(self.left_frame, text="Choose carrier image", command=self.load_carrier_file)
        self.carrier_image_button.pack()

        # Class members related to the secret image
        self.secret_fname = StringVar()
        self.secret_fname.set("images/jojo_meme_002.png")
        self.secret_label = ttk.Label(self.left_frame, textvariable=self.secret_fname)
        self.secret_label.pack()
        self.secret_image_button = ttk.Button(self.left_frame, text="Choose secret image", command=self.load_secret_file)
        self.secret_image_button.pack()

        self.stego_img_fname = StringVar()
        self.stego_img_fname.set("Enter save filename here")
        self.stego_img_entry = ttk.Entry(self.left_frame, textvariable=self.stego_img_fname)
        self.stego_img_entry.pack()
        self.stego_button = ttk.Button(self.left_frame, text="Hide secret image in carrier image", command=self.steno_image)
        self.stego_button.pack()

    def load_carrier_file(self):
        open_file_and_update_label(self.carrier_fname, self.carrier_label)

    def load_secret_file(self):
        open_file_and_update_label(self.secret_fname, self.secret_label)

    def load_hidden_file(self):
        open_file_and_update_label(self.hidden_fname, self.hidden_label)

    def load_encryption_key_file(self):
        self.encrypt_key_fname.set(filedialog.askopenfilename())
        key_in_byte_format = get_raw_bytes_from_file(self.encrypt_key_fname.get())
        key_string = "".join(map(chr, key_in_byte_format))
        self.encrypt_key_fname.set(key_string)
        self.encrypt_key_label["textvariable"] = self.encrypt_key_fname

    def load_decryption_key_file(self):
        self.decrypt_key_fname.set(filedialog.askopenfilename())
        key_in_byte_format = get_raw_bytes_from_file(self.decrypt_key_fname.get())
        key_string = "".join(map(chr, key_in_byte_format))
        self.decrypt_key_fname.set(key_string)
        self.decrypt_key_file_label["textvariable"] = self.decrypt_key_fname

        pass

    def generate_key(self):
        self.encryption_key = generate_key(16)
        key_string = "".join(map(chr, self.encryption_key))
        self.encrypt_key_fname.set(key_string)
        self.encrypt_key_label["textvariable"] = self.encrypt_key_fname

    def steno_image(self):
        if self.carrier_fname.get() == "" or self.secret_fname == "":
            return
        width, height = get_image_size(self.carrier_fname.get())

        # Opens the secret image and converts it into a byte array
        img_byte_array = get_raw_bytes_from_file(self.secret_fname.get())

        stenod_image = steno_image(self.encryption_key, img_byte_array, self.carrier_fname.get())
        save_bytes_to_image(stenod_image, self.stego_img_entry.get(), width, height)

    def unsteno_image(self):
        hidden = self.hidden_fname.get()
        width, height = get_image_size(hidden)
        img_byte_array = get_raw_bytes_from_file(hidden)
        extracted_secret = unsteno_image(self.encryption_key, hidden)
        save_bytes_to_file("images/output.png", extracted_secret)


if __name__ == '__main__':
    root = Tk()
    root.title("Steganography")
    root.minsize(200, 200)
    app = Application(master=root)
    app.mainloop()