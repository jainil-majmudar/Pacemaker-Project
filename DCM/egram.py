import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pacemaker_interface import PacemakerInterface as PI

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
        self.log_out = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.log_out.place(x=1000, y=30)

        self.back_button = tk.Button(root, text="Back", width='10', border=2, font=("Inter", 10, 'bold'), fg='white', bg='black', cursor='hand2', command=lambda: self.main.route(self.main.mode_sel))
        self.back_button.place(x=900, y=30)
