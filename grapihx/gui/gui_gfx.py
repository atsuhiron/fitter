import tkinter as tk

from grapihx.base_gfx import BaseGfx


class GuiGfx(BaseGfx):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fitter")

    def start(self):
        self.root.mainloop()

    def end(self):
        pass


if __name__ == "__main__":
    gg = GuiGfx()
    gg.start()
    