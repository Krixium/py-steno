from tkinter import *
from tkinter import ttk, filedialog

from PIL import ImageTk, Image

if __name__ == '__main__':
    root = Tk()
    root.title("Stenography")

    main_frame = ttk.Frame(root)
    main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    img = Image.open("images/jojo_meme_001.png")
    img = img.resize((250, 250), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img)
    cover_label = ttk.Label(main_frame, image=img2).grid(column=2, row=2, sticky=(W, E))

    message = StringVar()
    message_entry = ttk.Entry(main_frame, width=7, textvariable=message)
    message_entry.grid(column=1, row=1, sticky=(W, E))
    ttk.Label(main_frame, text="Message").grid(column=2, row=1, sticky=W)

    root.mainloop()
