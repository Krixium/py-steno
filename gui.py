from tkinter import *
from tkinter import ttk, filedialog

from PIL import ImageTk, Image

from dcutils import generate_key


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.key_label = ttk.Label(self)
        self.key_label.pack()

        self.key = 1

        self.keyvar = StringVar()
        self.keyvar.set("Key not generated")

        self.key_label["textvariable"] = self.keyvar

        self.key_button = ttk.Button(self)
        self.key_button["text"] = "Generate Key"
        self.key_button["command"] = self.generate_key
        self.key_button.pack()

    def generate_key(self):
        self.key = generate_key(16)
        key_string = "".join(map(chr, self.key))
        self.keyvar.set(key_string)
        self.key_label["textvariable"] = self.keyvar



if __name__ == '__main__':
    root = Tk()
    root.title("Stenography")
    root.minsize(200, 200)
    app = Application(master=root)
    app.mainloop()
