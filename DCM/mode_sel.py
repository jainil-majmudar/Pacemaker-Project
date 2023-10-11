import tkinter as tk
import json
import tkinter.messagebox as messagebox

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

        self.back_button = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.back_button.place(x=1000, y=20)

        # Create a dictionary to map modes to their parameters
        self.mode_parameters = {
            "AOO": ["Upper Rate Limit", "Lower Rate Limit", "Atrial Amplitude", "Atrial Pulse Width"],
            "VOO": ["Upper Rate Limit", "Lower Rate Limit", "Ventricular Amplitude", "Ventricular Pulse Width"],
            "AAI": ["Upper Rate Limit", "Lower Rate Limit", "Atrial Amplitude", "Atrial Pulse Width", "ARP"],
            "VVI": ["Upper Rate Limit", "Lower Rate Limit", "Ventricular Amplitude", "Ventricular Pulse Width", "VRP"]
        }

        self.current_widgets = []  # To store current widgets for mode parameters

    def render(self, mode):
        # Clear existing widgets
        for widget in self.current_widgets:
            widget.destroy()
        
        if mode in self.mode_parameters:
            parameters = self.mode_parameters[mode]
            row = 70  # Adjust the starting Y position
            for param in parameters:
                label = tk.Label(self.root, text=param)
                label.place(x=100, y=row)
                entry = tk.Entry(self.root)
                entry.place(x=250, y=row)
                self.current_widgets.extend([label, entry])
                row += 30  # Adjust the vertical spacing

        else:
            pass

