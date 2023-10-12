import tkinter as tk

class ModeSel:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app

        self.mode_label = tk.Label(root, text="Select Mode")
        self.mode_label.place(x=100, y=30)
        self.mode_var = tk.StringVar()
        modes = ["AOO", "VOO", "AAI", "VVI"]
        mode_dropdown = tk.OptionMenu(root, self.mode_var, *modes)
        mode_dropdown.place(x=200, y=30)
        next_button = tk.Button(root, text="Next", command=lambda: self.render(self.mode_var.get()))
        next_button.place(x=400, y=30)

        # Create a dictionary to map modes to their parameters
        self.mode_parameters = {
            "AOO": ["Lower Rate Limit", "Upper Rate Limit","Atrial Amplitude", "Atrial Pulse Width"],
            "VOO": ["Lower Rate Limit", "Upper Rate Limit","Ventricular Amplitude", "Ventricular Pulse Width"],
            "AAI": ["Lower Rate Limit", "Upper Rate Limit","Atrial Amplitude", "Atrial Pulse Width", "Atrial Sensitivity", "ARP", "PVARP", "Hysteresis", "Rate Smoothing"],
            "VVI": ["Lower Rate Limit", "Upper Rate Limit","Ventricular Amplitude", "Ventricular Pulse Width", "Ventricular Sensitivity", "VRP", "Hysteresis", "Rate Smoothing"]
        }

        self.current_widgets = []  # To store current widgets for mode parameters

    def update_scale_resolution(self, scale, current_value):
        # Define the range and corresponding resolutions
        ranges_and_resolutions = [(30, 50, 5), (50, 90, 1), (90, 175, 5)]

        # Determine the appropriate resolution for the current position
        for start, end, resolution in ranges_and_resolutions:
            if start <= current_value <= end:
                scale.config(resolution=resolution)
                break

    def render(self, mode):
        # Clear existing widgets
        for widget in self.current_widgets:
            widget.destroy()

        if mode in self.mode_parameters:
            parameters = self.mode_parameters[mode]
            row = 100  # Adjust the starting Y position
            for param in parameters:
                label = tk.Label(self.root, text=param)
                label.place(x=100, y=row)

                if param == "Lower Rate Limit":
                    # Create a single slider for Rate Limit with dynamic resolution
                    scale = tk.Scale(self.root, from_=30, to=175, orient="horizontal", resolution=5,length=400)
                    scale.set(60)  # Set the initial value
                    scale.place(x=250, y=row-15)
                    # Bind an update function to change resolution based on the slider position
                    scale.bind("<Motion>", lambda event, scale=scale: self.update_scale_resolution(scale, scale.get()))
                elif param == "Upper Rate Limit":
                    scale = tk.Scale(self.root, from_=50, to=175, resolution=5, orient="horizontal",length=400)
                    scale.set(120)
                    scale.place(x=250, y=row-15)
                elif param in ["Atrial Amplitude", "Ventricular Amplitude"]:
                    # Create a slider for Amplitude parameters
                    scale = tk.Scale(self.root, from_=0, to=7.0, resolution=0.1, orient="horizontal",length=400)
                    scale.set(3.5)
                    scale.place(x=250, y=row-15)
                elif param in ["Atrial Pulse Width", "Ventricular Pulse Width"]:
                    # Create a slider for Amplitude parameters
                    scale = tk.Scale(self.root, from_=0.05, to=1.9, resolution=0.1, orient="horizontal",length=400)
                    scale.set(0.4)
                    scale.place(x=250, y=row-15)
                elif param in ["Atrial Sensitivity", "Ventricular Sensitivity"]:
                    # Create a slider for Amplitude parameters
                    scale = tk.Scale(self.root, from_=0.25, to=10, resolution=0.1, orient="horizontal",length=400)
                    if(param == "Atrial Sensitivity"):
                        scale.set(0.75)
                    else:
                        scale.set(2.5)
                    scale.place(x=250, y=row-15)
                elif param == "VRP":
                    # Create a single slider for Rate Limit with dynamic resolution
                    scale = tk.Scale(self.root, from_=150, to=500, orient="horizontal", resolution=10,length=400)
                    scale.set(320)  # Set the initial value
                    scale.place(x=250, y=row-15)
                elif param == "ARP":
                    # Create a single slider for Rate Limit with dynamic resolution
                    scale = tk.Scale(self.root, from_=150, to=500, orient="horizontal", resolution=10,length=400)
                    scale.set(250)  # Set the initial value
                    scale.place(x=250, y=row-15)
                elif param =="PVARP":
                    # Create a single slider for Rate Limit with dynamic resolution
                    scale = tk.Scale(self.root, from_=150, to=500, orient="horizontal", resolution=10,length=400)
                    scale.set(250)  # Set the initial value
                    scale.place(x=250, y=row-15)
                elif param == "Hysteresis":
                    # Create a single slider for Rate Limit with dynamic resolution
                    scale = tk.Scale(self.root, from_=0, to=175, orient="horizontal", resolution=10,length=400)
                    scale.set(0)  # Set the initial value
                    scale.place(x=250, y=row-15)
                elif param == "Rate Smoothing":
                    # Create a single slider for Rate Limit with dynamic resolution
                    scale = tk.Scale(self.root, from_=0, to=25, orient="horizontal", resolution=10,length=400)
                    scale.set(0)  # Set the initial value
                    scale.place(x=250, y=row-15)
             
                

                self.current_widgets.extend([label, scale])
                row += 50  # Adjust the vertical spacing

        else:
            pass

