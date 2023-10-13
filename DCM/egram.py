import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Egram:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app

        # Create a Figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Set labels for the x and y axes
        self.ax.set_xlabel('Time (ms)')
        self.ax.set_ylabel('Voltage (mV)')

        # Create a canvas to display the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)

        # Place the canvas in the center of the root frame
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)