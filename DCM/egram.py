import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from serial_communication import SerialCommunication
from datetime import datetime


class Egram:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app
        self.serial_comm= SerialCommunication(self.main)

        # Create a Figure with two subplots
        self.fig = Figure(figsize=(10, 4), dpi=100, facecolor=self.main.bgcolor2)
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
        self.canvas_widget.config(bg=self.main.bgcolor2)
        self.canvas_widget.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        self.log_out = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=self.log_out_command)
        self.log_out.place(x=1000, y=30)

        self.back_button = tk.Button(root, text="Back", width='10', border=2, font=("Inter", 10, 'bold'), fg='white', bg='black', cursor='hand2', command=self.back_button_command)
        self.back_button.place(x=900, y=30)

        self.mode_label = tk.Label(root, font=("Inter", 10, 'bold'), fg='black', bg=self.main.bgcolor2, cursor='hand2',text="Select Mode")
        self.mode_label.place(x=100, y=30)
        self.mode_var = tk.StringVar()
        self.current_mode = ""
        self.modes = ["Atrial", "Ventricular", "Atrial + Ventricular"]
        self.mode_dropdown = tk.OptionMenu(root, self.mode_var, *self.modes)
        self.mode_dropdown.config(bg="blue", fg="white")
        self.mode_dropdown["menu"].config(bg="blue", fg='white')
        self.mode_dropdown.place(x=100, y=60)
        self.next_button = tk.Button(root, text="Next", font=("Inter", 10, 'bold'), fg='white', bg='blue', cursor='hand2', command=lambda: self.render(self.mode_var.get()))
        self.next_button.place(x=250, y=60)

        self.lines_atrial = []
        self.lines_ventricular = []

        # Hide the plots initially
        self.ax_atrial.set_visible(False)
        self.ax_ventricular.set_visible(False)

        self.timer_interval = 5  # Time interval in milliseconds
        self.egram_data = {'Atrial': [], 'Ventricular': []}  # Placeholder for Egram data

        self.stop_button = tk.Button(root, text="Start/Stop", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=self.toggle_egram)
        self.stop_button.place(x=360, y=60)

        self.stop_graph = False

    def render(self, mode):
        if (self.current_mode == "Atrial" and mode == "Ventricular") or \
           (self.current_mode == "Atrial" and mode == "Atrial + Ventricular") or \
           (self.current_mode == "Ventricular" and mode != "Atrial + Ventricular") or \
           (self.current_mode == "Ventricular" and mode != "Atrial") or \
           (self.current_mode == "Atrial + Ventricular" and mode != "Atrial") or \
           (self.current_mode == "Atrial + Ventricular" and mode != "Ventricular"):
            # Stop the graph in the previous mode if it is running
            self.stop_egram()

        # Update the current mode
        self.current_mode = mode

        # Clear existing lines if any
        for line in self.lines_atrial:
            line.remove()
        for line in self.lines_ventricular:
            line.remove()
        self.lines_atrial = []
        self.lines_ventricular = []

        # Capture the start time
        start_time = datetime.now()

        # Show the selected plot
        if mode == "Atrial":
            # Create blank atrial graph
            self.ax_atrial.plot([], [])
            self.ax_atrial.set_visible(True)
            
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

        # Start a loop to continuously update the Egram data
        self.update_egram_data(mode, start_time)
    
    def update_egram_data(self, mode, start_time):
        # Fetch Egram data from the pacemaker using send_parameters method
        new_egram_data = self.serial_comm.send_parameters({'MODE': 1, 'LRL': 60, 'URL': 120, 'MSR': 120, 'A_AMPLITUDE': 2.0,
                                                            'V_AMPLITUDE': 5.0, 'A_WIDTH': 1, 'V_WIDTH': 1,
                                                            'A_SENSITIVITY': 3.0, 'V_SENSITIVITY': 3.0, 'VRP': 320,
                                                            'ARP': 250, 'ACTIVITY_THRESH': 'med', 'REACT_TIME': 30,
                                                            'RESPONSE_FAC': 8, 'RECOVERY_TIME': 5}, b'\x00', b'\x02')

        if not self.stop_graph:
            # Calculate the elapsed time
            elapsed_time = datetime.now() - start_time

            if mode == "Atrial":
                self.egram_data['Atrial'].append((elapsed_time, new_egram_data[0]))
                self.update_subplot(self.ax_atrial, self.egram_data['Atrial'], 'Atrial')
            elif mode == "Ventricular":
                self.egram_data['Ventricular'].append((elapsed_time, new_egram_data[1]))
                self.update_subplot(self.ax_ventricular, self.egram_data['Ventricular'], 'Ventricular')
            elif mode == "Atrial + Ventricular":
                # Assuming new_egram_data contains both atrial and ventricular data
                self.egram_data['Atrial'].append((elapsed_time, new_egram_data[0]))
                self.egram_data['Ventricular'].append((elapsed_time, new_egram_data[1]))
                self.update_subplot(self.ax_atrial, self.egram_data['Atrial'], 'Atrial')
                self.update_subplot(self.ax_ventricular, self.egram_data['Ventricular'], 'Ventricular')

            # Schedule the next update after the specified time interval
            self.root.after(self.timer_interval, self.update_egram_data, mode, start_time)

    def update_subplot(self, axis, new_data, plot_title):
        # Clear the axis
        axis.clear()

        # Extract timestamps and data
        timestamps, voltage_data = zip(*new_data)

        # Calculate the elapsed time in seconds for each data point
        elapsed_times = [(timestamp - timestamps[0]).total_seconds() for timestamp in timestamps]

        # Plot the data
        axis.plot(elapsed_times, voltage_data, 'b-')
        axis.set_title(plot_title)

        # Set x-axis limits dynamically based on elapsed time
        max_elapsed_time = max(elapsed_times)
        min_elapsed_time = max(0, max_elapsed_time - 15)  # Keep a time frame of 50 seconds
        axis.set_xlim(min_elapsed_time, max_elapsed_time)

        # Redraw the canvas
        self.canvas.draw()


    def toggle_egram(self):
        # Toggle the stop_graph flag
        self.stop_graph = not self.stop_graph

        if not self.stop_graph:
            # Record the start time when resuming
            self.start_time = datetime.now()
            self.egram_data = {'Atrial': [], 'Ventricular': []}
            self.update_egram_data(self.current_mode, start_time=self.start_time)


    def stop_egram(self):
        # Set the stop_graph flag to True
        self.stop_graph = True

    def log_out_command(self):
        # Stop the graphs when Log Out button is pressed
        self.stop_egram()
        self.main.route(self.main.login_frame)

    def back_button_command(self):
        # Stop the graphs when Back button is pressed
        self.stop_egram()
        self.main.route(self.main.mode_sel)
