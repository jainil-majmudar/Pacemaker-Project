import tkinter as tk
import json
import tkinter.messagebox as messagebox

class ModeSel:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app
        self.error_labels = {}

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

        # Initialize the parameter values dictionary with default values
        self.parameter_values = {
            "Lower Rate Limit": 60,
            "Upper Rate Limit": 120,
            "Atrial Amplitude": 3.5,
            "Atrial Pulse Width": 0.4,
            "Atrial Sensitivity": 0.75,
            "Ventricular Amplitude": 3.5,
            "Ventricular Pulse Width": 0.4,
            "Ventricular Sensitivity": 2.5,
            "ARP": 250,
            "VRP": 320,
            "PVARP": 250,
            "Hysteresis": 0,
            "Rate Smoothing": 0
        }

    def render(self, mode):
        chosen_pacemaker = self.main.pacemaker_interface.pacemaker_entry.get()  # Get the selected pacemaker from the main app
        self.pacemaker = chosen_pacemaker
        # Clear existing widgets and reset error labels
        for widget in self.current_widgets:
            widget.destroy()

        for param, error_label in self.error_labels.items():
            error_label.config(text="")  # Reset the error label text to clear errors

        if mode in self.mode_parameters:
            parameters = self.mode_parameters[mode]
            row = 70  # Adjust the starting Y position
            for param in parameters:
                label = tk.Label(self.root, text=param)
                label.place(x=100, y=row)
                entry = tk.Entry(self.root)
                entry.place(x=250, y=row)
                self.current_widgets.extend([label, entry])

                # Set the initial value from the parameter_values dictionary
                entry.insert(0, str(self.parameter_values[param]))

                # Bind the entry to a function that updates the parameter_values dictionary and displays error messages
                entry.bind("<FocusOut>", lambda event, entry=entry, param=param: self.update_parameter_value(entry, param))

                # Create an error label next to the entry (initially empty)
                error_label = tk.Label(self.root, text="", fg="red", bg="#F5E8B7")
                error_label.place(x=450, y=row)
                self.error_labels[param] = error_label  # Store the error label for later use
                row += 30  # Adjust the vertical spacing

        # Update parameter_values with the selected pacemaker
        self.parameter_values['Pacemaker'] = chosen_pacemaker

        submit_button = tk.Button(self.root, text="Submit Parameters", command=self.show_parameter_values)
        submit_button.place(x=250, y=row)
        self.current_widgets.append(submit_button)

    def validate_lower_rate_limit(self, value):
        try:
            value = float(value)
            if 30 <= value <= 175:
                if 30 <= value <= 50:
                    if value % 5 == 0:
                        return True
                    else:
                        return "Lower Rate Limit should be a multiple of 5 between 30 and 50."
                elif 50 < value <= 90:
                    if value.is_integer():
                        return True
                    else:
                        return "Lower Rate Limit should be an integer between 50 and 90."
                else:
                    if 90 <= value <= 175:
                        if value % 5 == 0:
                            return True
                        else:
                            return "Lower Rate Limit should be a multiple of 5 between 90 and 175."
            else:
                return "Lower Rate Limit should be between 30 and 175."
        except ValueError:
            return "Lower Rate Limit should be a valid number."
     

    def update_parameter_value(self, entry, param):
        value = entry.get()
        # Perform validation for each parameter here if needed
        if param == "Lower Rate Limit":
            if self.validate_lower_rate_limit(value) == "True":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_lower_rate_limit(value)
        else:
            try:
                value = float(value)
                self.parameter_values[param] = value
                self.error_labels[param]["text"] = ""  # Clear the error message
            except ValueError:
                pass

    def store_parameter_values(self):
    # Load existing JSON data
        try:
            with open("DCM/DataStorage/pacemaker_data.json", "r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            json_data = {}

        # Get the selected pacemaker and mode
        selected_pacemaker = self.parameter_values['Pacemaker']
        selected_mode = self.mode_var.get()

        # Filter the parameter_values dictionary to include only the parameters for the selected mode
        selected_mode_params = {param: value for param, value in self.parameter_values.items() if param in self.mode_parameters[selected_mode]}

        # Check if there is an entry for the selected pacemaker
        if selected_pacemaker in json_data:
            # Update the existing entry with the new parameter values
            json_data[selected_pacemaker][selected_mode] = selected_mode_params
        else:
            # Create a new entry for the selected pacemaker
            json_data[selected_pacemaker] = {selected_mode: selected_mode_params}

        # Save the updated JSON data back to the file
        with open("DCM/DataStorage/pacemaker_data.json", "w") as file:
            json.dump(json_data, file)

        print(f"Stored parameter values for pacemaker '{selected_pacemaker}' for the selected mode '{selected_mode}'.")

    def show_parameter_values(self):
        # Update parameter_values with the selected pacemaker
        self.parameter_values['Pacemaker'] = self.pacemaker
        self.store_parameter_values()

        # Filter the parameter_values dictionary to include only the parameters for the selected mode
        selected_mode_params = {param: value for param, value in self.parameter_values.items() if param in self.mode_parameters[self.mode_var.get()]}

        print("Parameter values:", selected_mode_params)
        # You can now use the parameter values as needed