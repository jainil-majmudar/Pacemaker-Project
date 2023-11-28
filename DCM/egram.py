import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from serial_communication import SerialCommunication


class Egram:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app
        self.serial_comm= SerialCommunication(self.main)

        # Create a Figure with two subplots
        self.fig = Figure(figsize=(10, 4), dpi=100, facecolor='#F5E8B7')
        self.ax_atrial = self.fig.add_subplot(121)
        self.ax_ventricular = self.fig.add_subplot(122)

        # Set labels for the x and y axes
        self.ax_atrial.set_xlabel('Time (ms)')
        self.ax_atrial.set_ylabel('Voltage (mV)')
        self.ax_ventricular.set_xlabel('Time (ms)')
        self.ax_ventricular.set_ylabel('Voltage (mV)')

        # Create a canvas to display the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)

        # Place the canvas in the center of the root frame
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(bg='#F5E8B7')
        self.canvas_widget.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        self.log_out = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.log_out.place(x=1000, y=30)

        self.back_button = tk.Button(root, text="Back", width='10', border=2, font=("Inter", 10, 'bold'), fg='white', bg='black', cursor='hand2', command=lambda: self.main.route(self.main.mode_sel))
        self.back_button.place(x=900, y=30)

        self.mode_label = tk.Label(root, font=("Inter", 10, 'bold'), fg='black', bg='#F5E8B7', cursor='hand2',text="Select Mode")
        self.mode_label.place(x=100, y=30)
        self.mode_var = tk.StringVar()
        self.current_mode = ""
        self.modes = ["Atrial", "Ventricular", "Atrial + Ventricular"]
        self.mode_dropdown = tk.OptionMenu(root, self.mode_var, *self.modes)
        self.mode_dropdown.config(bg="blue", fg="white")
        self.mode_dropdown["menu"].config(bg="blue", fg='white')
        self.mode_dropdown.place(x=100, y=60)
        next_button = tk.Button(root, text="Next", font=("Inter", 10, 'bold'), fg='white', bg='blue', cursor='hand2', command=lambda: self.render(self.mode_var.get()))
        next_button.place(x=250, y=60)

        self.lines_atrial = []
        self.lines_ventricular = []

        # Hide the plots initially
        self.ax_atrial.set_visible(False)
        self.ax_ventricular.set_visible(False)

    def render(self, mode):
        self.current_mode = mode
        chosen_pacemaker = self.main.pacemaker_interface.pacemaker_entry.get()
        self.pacemaker = chosen_pacemaker

        # Clear existing lines if any
        for line in self.lines_atrial:
            line.remove()
        for line in self.lines_ventricular:
            line.remove()
        self.lines_atrial = []
        self.lines_ventricular = []

        # Show the selected plot
        if mode == "Atrial":
            # Create blank atrial graph
            self.ax_atrial.plot([], [])
            self.ax_atrial.set_visible(True)
            data = self.serial_comm.send_parameters({'MODE': 1, 'LRL': 60, 'URL': 120, 'MSR': 120, 'A_AMPLITUDE': 2.0,
                                                            'V_AMPLITUDE': 5.0, 'A_WIDTH': 1, 'V_WIDTH': 1,
                                                            'A_SENSITIVITY': 0.0, 'V_SENSITIVITY': 0.0, 'VRP': 320,
                                                            'ARP': 250, 'HRL': 0, 'RATE_SMOOTH': 0,
                                                            'ACTIVITY_THRESH': 'med', 'REACT_TIME': 30,
                                                            'RESPONSE_FAC': 8, 'RECOVERY_TIME': 5},b'\x00',b'\x01')
            
            # Adjust the position of ax_atrial to move it towards the middle
            bbox_atrial = self.ax_atrial.get_position()
            bbox_atrial.x0 = 0.28
            bbox_atrial.x1 = 0.75
            self.ax_atrial.set_position(bbox_atrial)
        else:
            # Hide atrial subplot if not in atrial mode
            self.ax_atrial.set_visible(False)

        if mode == "Ventricular":
            # Create blank ventricular graph (graph 2)
            self.ax_ventricular.plot([], [])
            self.ax_ventricular.set_visible(True)

            # Adjust the position of ax_atrial to move it towards the middle
            bbox_ventricular = self.ax_ventricular.get_position()
            bbox_ventricular.x0 = 0.28
            bbox_ventricular.x1 = 0.75
            self.ax_ventricular.set_position(bbox_ventricular)
        else:
            # Hide ventricular subplot if not in ventricular mode
            self.ax_ventricular.set_visible(False)

        if mode == "Atrial + Ventricular":
            # Create blank ventricular graph (graph 2)
            self.ax_atrial.plot([], [])
            self.ax_atrial.set_visible(True)
            self.ax_ventricular.plot([], [])
            self.ax_ventricular.set_visible(True)

            # Adjust the position of ax_atrial to move it towards the middle
            bbox_atrial = self.ax_atrial.get_position()
            bbox_atrial.x0 = 0.1
            bbox_atrial.x1 = 0.45
            self.ax_atrial.set_position(bbox_atrial)
            bbox_ventricular = self.ax_ventricular.get_position()
            bbox_ventricular.x0 = 0.55
            bbox_ventricular.x1 = 0.9
            self.ax_ventricular.set_position(bbox_ventricular)


        # Update legends and redraw the canvas
        self.canvas.draw()
        # self.ax_atrial.legend()
        # self.ax_ventricular.legend()
