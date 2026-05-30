

import tkinter as tk
from gui import AlbumGeneratorApp


def main():

    root = tk.Tk()


    try:
        root.iconbitmap(default="")
    except tk.TclError:
        pass


    app = AlbumGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
