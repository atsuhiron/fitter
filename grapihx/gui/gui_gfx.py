import tkinter.ttk as ttk
import tkinter as raw_tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

from grapihx.base_gfx import BaseGfx


class DynamicFrame(ttk.Frame):
    def __init__(self, master):
        main_grid_param = {
            "padx": 6,
            "pady": 6
        }
        super(DynamicFrame, self).__init__(master)
        self.master = master

        frame = ttk.Frame(self.master)

        # main board
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=frame)

        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=raw_tk.BOTH, expand=True)
        frame.grid(column=0, row=0, **main_grid_param)

        # draw canvas
        self.x_arr = np.linspace(-np.pi, np.pi, 128)
        self.y_arr = DynamicFrame.sin(self.x_arr, 1.0)
        self.ax_plot, = self.ax.plot(self.x_arr, self.y_arr)
        self.fig_canvas.draw()

        # sidebar
        self.side_bar = ttk.Frame(self.master)
        self.side_bar.grid(column=1, row=0, **main_grid_param)

        # button
        button = ttk.Button(self.side_bar, text="Reset", command=self.reset)
        button.pack()

        # slider
        self.val1 = raw_tk.DoubleVar()
        self.val1.set(1.0)
        self.sli1 = ttk.Scale(
            self.side_bar, variable=self.val1, orient=raw_tk.HORIZONTAL, length=300,# resolution=0.2,
            from_=-5, to=5, command=self.on_slide
        )
        self.sli1.pack()

    def reset(self):
        self.val1.set(1.0)
        self.draw(1.0)

    def on_slide(self, e):
        self.draw(float(e))

    def draw(self, *args):
        self.y_arr = DynamicFrame.sin(self.x_arr, args[0])
        self.ax_plot.set_ydata(self.y_arr)
        self.fig_canvas.draw()

    @staticmethod
    def sin(x, freq) -> np.ndarray:
        return np.sin(x * freq)


class DynamicFrame2D(ttk.Frame):
    INIT_VAL: float = 1.0
    def __init__(self, master):
        main_grid_param = {
            "padx": 6,
            "pady": 6
        }
        super(DynamicFrame2D, self).__init__(master)
        self.master = master

        frame = ttk.Frame(self.master)

        # main board
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=frame)

        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=raw_tk.BOTH, expand=True)
        frame.grid(column=0, row=0, **main_grid_param)

        # draw canvas
        _arr = np.linspace(-np.pi, np.pi, 128)

        self.x_mesh, self.y_mesh = np.meshgrid(_arr, _arr)
        self.z_mesh = DynamicFrame2D.sincos(self.x_mesh, self.y_mesh, DynamicFrame2D.INIT_VAL, DynamicFrame2D.INIT_VAL)
        self.ax_plot = self.ax.imshow(self.z_mesh)
        self.fig_canvas.draw()

        # sidebar
        self.side_bar = ttk.Frame(self.master)
        self.side_bar.grid(column=1, row=0, **main_grid_param)

        # button
        button = ttk.Button(self.side_bar, text="Reset", command=self.reset)
        button.pack()

        # slider
        self.val_s = raw_tk.DoubleVar()
        self.val_s.set(DynamicFrame2D.INIT_VAL)
        self.sli_s = ttk.Scale(
            self.side_bar, variable=self.val_s, orient=raw_tk.HORIZONTAL, length=300,
            from_=-5, to=5, command=self.on_slide_s
        )
        self.sli_s.pack()

        self.val_c = raw_tk.DoubleVar()
        self.val_c.set(DynamicFrame2D.INIT_VAL)
        self.sli_c = ttk.Scale(
            self.side_bar, variable=self.val_c, orient=raw_tk.HORIZONTAL, length=300,
            from_=-5, to=5, command=self.on_slide_c
        )
        self.sli_c.pack()

    def reset(self):
        self.val_s.set(DynamicFrame2D.INIT_VAL)
        self.val_c.set(DynamicFrame2D.INIT_VAL)
        self.draw(DynamicFrame2D.INIT_VAL, DynamicFrame2D.INIT_VAL)

    def on_slide_s(self, e):
        self.draw(float(e), self.val_c.get())

    def on_slide_c(self, e):
        self.draw(self.val_s.get(), float(e))

    def draw(self, *args):
        self.z_mesh = DynamicFrame2D.sincos(self.x_mesh, self.y_mesh, *args)
        self.ax_plot.set_data(self.z_mesh)
        self.fig_canvas.draw()

    @staticmethod
    def sincos(x, y, freq_s, freq_c) -> np.ndarray:
        return np.sin(x * freq_s) * np.cos(y * freq_c)


class GuiGfx(BaseGfx):
    def __init__(self):
        self.root = raw_tk.Tk()
        self.root.title("Fitter")
        self.dynamic_frame = DynamicFrame2D(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.end)

    def start(self):
        self.root.mainloop()

    def end(self):
        self.clear_fig()
        self.root.destroy()
        self.root.quit()

    @staticmethod
    def clear_fig():
        plt.clf()


if __name__ == "__main__":
    gg = GuiGfx()
    gg.start()
