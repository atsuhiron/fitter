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

        # main board
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig_canvas = FigureCanvasTkAgg(self.fig, frame)

        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        frame.pack()

        # draw canvas
        self.x_arr = np.linspace(-np.pi, np.pi, 64)
        self.y_arr = DynamicFrame.sin(self.x_arr, 1.0)
        self.ax_plot, = self.ax.plot(self.x_arr, self.y_arr)
        self.fig_canvas.draw()

        # button
        button = tk.Button(self.master, text="Draw Graph", command=self.button_click)
        button.pack(side=tk.BOTTOM)

        # slider
        self.val1 = tk.DoubleVar()
        self.sli1 = tk.Scale(
            frame, variable=self.val1, orient=tk.HORIZONTAL, length=300, resolution=0.2,
            from_=-5, to=5, command=self.on_slide
        )
        self.sli1.pack()

    def button_click(self):
        x = np.arange(-np.pi, np.pi, 0.1)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.fig_canvas.draw()

    def on_slide(self, e):
        self.y_arr = DynamicFrame.sin(self.x_arr, self.val1.get())
        self.ax_plot.set_ydata(self.y_arr)
        self.fig_canvas.draw()

    @staticmethod
    def sin(x, freq) -> np.ndarray:
        return np.sin(x * freq)


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
    