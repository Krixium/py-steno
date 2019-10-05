from tkinter import *
from tkinter import ttk, filedialog

from PIL import ImageTk, Image

from dcutils import generate_key
from dcstego import steno_image, unsteno_image
from dcimage import get_bytes_from_image, save_bytes_to_image, get_image_size

import io

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
        self.pack()

        # Defining class members related to key generation
        self.key = 1

        self.keyvar = StringVar()
        self.keyvar.set("Key not generated")

        self.key_label = ttk.Label(self)
        self.key_label.pack()
        self.key_label["textvariable"] = self.keyvar

        self.key_button = ttk.Button(self, text="Generate Key", command=self.generate_key)
        self.key_button.pack()

        # Defining class members related to the carrier image
        self.carrier_fname = StringVar()
        self.carrier_fname.set("images/jojo_meme_001.png")

        self.carrier_label = ttk.Label(self, textvariable=self.carrier_fname)
        self.carrier_label.pack()

        self.carrier_image_button = ttk.Button(self, text="Choose Carrier Image", command=self.load_carrier_file)
        self.carrier_image_button.pack()

        # Class members related to the secret image
        self.secret_fname = StringVar()
        self.secret_fname.set("images/jojo_meme_002.png")
        self.secret_label = ttk.Label(self, textvariable=self.secret_fname)
        self.secret_label.pack()
        self.secret_image_button = ttk.Button(self, text="Choose Secret Image", command=self.load_secret_file)
        self.secret_image_button.pack()

        self.stego_img_fname = StringVar()
        self.stego_img_fname.set("Enter save filename here")
        self.stego_img_entry = ttk.Entry(self, textvariable=self.stego_img_fname)
        self.stego_img_entry.pack()

        self.stego_button = ttk.Button(self, text="Hide Secret Image in Carrier Image", command=self.stego_image)
        self.stego_button.pack()


    def load_carrier_file(self):
        self.carrier_fname.set(filedialog.askopenfilename())
        self.carrier_label["textvariable"] = self.carrier_fname

    def load_secret_file(self):
        self.secret_fname.set(filedialog.askopenfilename())
        self.secret_label["textvariable"] = self.secret_fname

    def generate_key(self):
        self.key = generate_key(16)
        key_string = "".join(map(chr, self.key))
        self.keyvar.set(key_string)
        self.key_label["textvariable"] = self.keyvar
        # TODO: Export the key

    def stego_image(self):
        if self.carrier_fname.get() == "" or self.secret_fname == "":
            return
        width, height = get_image_size(self.carrier_fname.get())


        # Opens the secret image and converts it into a byte array
        img_byte_array = convert_image_to_byte_array(self.secret_fname.get())

        stenod_image = steno_image(self.key, img_byte_array, self.carrier_fname.get())
        save_bytes_to_image(stenod_image, self.stego_img_entry.get(), width, height)

    def unstego_image(self):
        pass



if __name__ == '__main__':
    root = Tk()
    root.title("Steganography")
    root.minsize(200, 200)
    app = Application(master=root)
    app.mainloop()
