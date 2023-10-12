import tkinter as tk
import json

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
            "AOO": ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width"],
            "VOO": ["Lower Rate Limit", "Upper Rate Limit", "Ventricular Amplitude", "Ventricular Pulse Width"],
            "AAI": ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width", "Atrial Sensitivity", "ARP", "PVARP", "Hysteresis", "Rate Smoothing"],
            "VVI": ["Lower Rate Limit", "Upper Rate Limit", "Ventricular Amplitude", "Ventricular Pulse Width", "Ventricular Sensitivity", "VRP", "Hysteresis", "Rate Smoothing"]
        }

        self.current_widgets = []  # To store current widgets for mode parameters
        self.parameter_values = {}  # Dictionary to store parameter values

    def render(self, mode):
        chosen_pacemaker = self.main.pacemaker_interface.pacemaker_entry.get()  # Get the selected pacemaker from the main app
        self.pacemaker = chosen_pacemaker
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

                # Bind the entry to a function that updates the parameter_values dictionary
                entry.bind("<FocusOut>", lambda event, entry=entry, param=param: self.update_parameter_value(entry, param))
                row += 30  # Adjust the vertical spacing

            # Update parameter_values with the selected pacemaker
            self.parameter_values['Pacemaker'] = chosen_pacemaker

            submit_button = tk.Button(self.root, text="Submit Parameters", command=self.show_parameter_values)
            submit_button.place(x=250, y=row)
            self.current_widgets.append(submit_button)

    def update_parameter_value(self, entry, param):
        value = entry.get()
        # Perform validation for each parameter here if needed
        # For example, you can check if value is a valid number
        try:
            value = float(value)
            self.parameter_values[param] = value
        except ValueError:
            pass
    def store_parameter_values(self):
            # Load existing JSON data
            try:
                with open("DCM/DataStorage/pacemaker_data.json", "r") as file:
                    json_data = json.load(file)
            except FileNotFoundError:
                json_data = {}

            # Get the selected pacemaker
            selected_pacemaker = self.parameter_values['Pacemaker']

            # Check if there is an entry for the selected pacemaker
            if selected_pacemaker in json_data:
                # Update the existing entry with the new parameter values
                json_data[selected_pacemaker].update(self.parameter_values)
            else:
                # Create a new entry for the selected pacemaker
                json_data[selected_pacemaker] = self.parameter_values

            # Save the updated JSON data back to the file
            with open("DCM/DataStorage/pacemaker_data.json", "w") as file:
                json.dump(json_data, file)

            print(f"Stored parameter values for pacemaker '{selected_pacemaker}'.")

    def show_parameter_values(self):
            # Update parameter_values with the selected pacemaker
            self.parameter_values['Pacemaker'] = self.pacemaker
            self.store_parameter_values()

            print("Parameter values:", self.parameter_values)
            # You can now use the parameter values as needed
