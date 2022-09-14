import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

from grapihx.base_gfx import BaseGfx


class DynamicFrame(tk.Frame):
    def __init__(self, master):
        super(DynamicFrame, self).__init__(master)
        self.master = master

        frame = tk.Frame(self.master)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig_canvas = FigureCanvasTkAgg(self.fig, frame)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        frame.pack()

        button = tk.Button(self.master, text="Draw Graph", command=self.button_click)
        button.pack(side=tk.BOTTOM)

    def button_click(self):
        x = np.arange(-np.pi, np.pi, 0.1)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.fig_canvas.draw()


class GuiGfx(BaseGfx):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fitter")
        self.dynamic_frame = DynamicFrame(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.end)

    def start(self):
        self.root.mainloop()

    def end(self):
        self.root.destroy()
        self.root.quit()


if __name__ == "__main__":
    gg = GuiGfx()
    gg.start()
    