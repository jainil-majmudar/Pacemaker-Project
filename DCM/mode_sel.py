import tkinter as tk
import json
import tkinter.messagebox as messagebox

class ModeSel:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app
        self.error_labels = {}

        self.mode_label = tk.Label(root, font=("Inter", 10, 'bold'), fg='black', bg='#F5E8B7', cursor='hand2',text="Select Mode")
        self.mode_label.place(x=100, y=30)
        self.mode_var = tk.StringVar()
        modes = ["AOO", "VOO", "AAI", "VVI"]
        mode_dropdown = tk.OptionMenu(root, self.mode_var, *modes)
        mode_dropdown.config(bg="blue", fg="white")
        mode_dropdown["menu"].config(bg="blue", fg = 'white')
        mode_dropdown.place(x=100, y=60)
        next_button = tk.Button(root, text="Next", font=("Inter", 10, 'bold'), fg='white', bg='blue', cursor='hand2', command=lambda: self.render(self.mode_var.get()))
        next_button.place(x=200, y=60)

        display_data_button = tk.Button(root, text = "Display Existing Data", font=("Inter", 10, 'bold'), fg='white', bg='green', cursor='hand2', command=lambda :self.main.route(self.main.display_frame))
        display_data_button.place(x=625, y=30)

        egram_button = tk.Button(root,text = "View Egram Data", font=("Inter", 10, 'bold'), fg='white', bg='green', cursor='hand2', command=lambda :self.main.route(self.main.egram_frame))
        egram_button.place(x=500,y=30)

        self.log_out = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.log_out.place(x=1000, y=30)

        self.back_button = tk.Button(root, text="Back", width='10', border=2, font=("Inter", 10, 'bold'), fg='white', bg='black', cursor='hand2', command=lambda: self.main.route(self.main.pacemaker_sel))
        self.back_button.place(x=900, y=30)

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
            "Hysteresis":0,
            "Rate Smoothing": 0
        }

    def render(self, mode):
        chosen_pacemaker = self.main.pacemaker_interface.pacemaker_entry.get()
        self.pacemaker = chosen_pacemaker

        # Clear existing widgets and reset error labels
        for widget in self.current_widgets:
            widget.destroy()

        self.current_widgets = []  # Reset the list

        for param, error_label in self.error_labels.items():
            error_label.config(text="")  # Reset the error label text to clear errors

        if mode in self.mode_parameters:
            parameters = self.mode_parameters[mode]
            row = 130  # Adjust the starting Y position
            for param in parameters:
                label = tk.Label(self.root, text=param, bg="#F5E8B7")
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
                        return "Valid"
                    else:
                        return "Lower Rate Limit should be a multiple of 5 if between 30ppm and 50ppm."
                elif 50 <= value <= 90:
                    if value.is_integer():
                        return "Valid"
                    else:
                        return "Lower Rate Limit should be an integer if between 50ppm and 90ppm."
                else:
                    if 90 <= value <= 175:
                        if value % 5 == 0:
                            return "Valid"
                        else:
                            return "Lower Rate Limit should be a multiple of 5 between 90ppm and 175ppm."
            else:
                return "Lower Rate Limit should be between 30ppm and 175ppm."
        except ValueError:
            return "Lower Rate Limit should be a valid value."
        

    def validate_upper_rate_limit(self, value):
        try:
            value = float(value)
            if 50 <= value <= 175:
                if value % 5 == 0:
                    return "Valid"
                else:
                    return "Upper Rate Limit should be a multiple of 5 between 50ppm and 175ppm."
            else:
                return "Upper Rate Limit should be between 50ppm and 175ppm."
        except ValueError:
            return "Upper Rate Limit should be a valid value."
     
    def validate_amplitude(self, value):
        try:
            value = float(value)
            if value==0:
                return "Valid"
            if value==0.5 or value==0.6 or value==0.7:
                return "Valid"
            elif 0.7 <= value <= 3.2:
                if value % 0.1 == 0:
                    return "Valid"
                else:
                    return "Amplitude should be a multiple of 0.1 if between 0.5V and 3.2V."
            elif 3.5 <= value <= 7.0:
                if value % 0.5 == 0:
                    return "Valid"
                else:
                    return "Amplitude should be a multiple of 0.5 if between 3.5V and 7.0V."
            else:
                return "Amplitude should be 0V or between 0.5V - 3.2V or 3.5V - 7.0V"
        except ValueError:
            return "Amplitude should be a valid value."
        
    def validate_pulse_width(self, value):
        try:
            value = float(value)
            if value==0.05:
                return "Valid"
            elif 0.1 <= value <= 1.9:
                if value % 0.1 == 0:
                    return "Valid"
                else:
                    return "Pulse Width should be a multiple of 0.1 if between 0.1ms and 1.9ms"
            else:
                return "Pulse Width should be either 0.05ms or a multiple of 0.1 between 0.1ms and 1.9ms"
        except ValueError:
            return "Pulse Width should be a valid value."

    def validate_sensitivity(self, value):
        try:
            value = float(value)
            if value == 0.25 or value == 0.5 or value == 0.75:
                return "Valid"
            elif 1.0 <= value <= 10.0:
                if value % 0.5 == 0:
                    return "Valid"
                else:
                    return "Sensitivity should be a multiple of 0.5 if between 1mV and 10mV."
            else:
                return "Sensitivity should be either 0.25mV, 0.5mV, 0.75mV or between 1mV and 10mV."
        except ValueError:
            return "Sensitivity should be a valid value."
        
    def validate_refractory_period(self, value):
        try:
            value = float(value)
            if 150 <= value <= 500:
                if value % 10 == 0:
                    return "Valid"
                else:
                    return "Refractory Period value should be a multiple of 10 between 150ms and 500ms."
            else: 
                return "Refractory Period value should be between 150ms and 500ms."
        except ValueError:
            return "Refractory Period value should be a valid value."

    def validate_hysteresis(self, value):
        try:
            value = float(value)
            if 0 <= value <= 175:
                if value==25 or value==0:
                    return "Valid"
                elif 30 <= value <= 50:
                    if value % 5 == 0:
                        return "Valid"
                    else:
                        return "Hysteresis should be a multiple of 5 if between 30ppm and 50ppm."
                elif 50 <= value <= 90:
                    if value.is_integer():
                        return "Valid"
                    else:
                        return "Hysteresis should be an integer if between 50ppm and 90ppm."
                else:
                    if 90 <= value <= 175:
                        if value % 5 == 0:
                            return "Valid"
                        else:
                            return "Hysteresis should be a multiple of 5 between 90ppm and 175ppm."
            else:
                return "Hysteresis should be between 0ppm and 175ppm."
        except ValueError:
            return "Hysteresis should be a valid value."
        
    def validate_rate_smoothing(self, value):
        try:
            value = int(value)
            if 0 <= value <= 21 or value == 25:
                if value % 3 == 0:
                    return "Valid"
                else:
                    return "Rate Smoothing should be one of these values-> 0%, 3%, 6%, 9%, 12%, 15%, 18%, 21%, 25%"
            else:
                return "Rate Smoothing should be one of these values-> 0%, 3%, 6%, 9%, 12%, 15%, 18%, 21%, 25%"
        except ValueError:
            return "Rate smoothing should be a valid percentage."

    def update_parameter_value(self, entry, param):
        value = entry.get()
        # Perform validation for each parameter here if needed
        if param == "Lower Rate Limit":
            if self.validate_lower_rate_limit(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = "" # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_lower_rate_limit(value)

        elif param == "Upper Rate Limit":
            if self.validate_upper_rate_limit(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_upper_rate_limit(value)

        elif param == "Atrial Amplitude":
            if self.validate_amplitude(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_amplitude(value)

        elif param == "Atrial Pulse Width":
            if self.validate_pulse_width(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_pulse_width(value)

        elif param == "Ventricular Amplitude":
            if self.validate_amplitude(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_amplitude(value)

        elif param == "Ventricular Pulse Width":
            if self.validate_pulse_width(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_pulse_width(value)

        elif param == "Atrial Sensitivity":
            if self.validate_sensitivity(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_sensitivity(value)

        elif param == "ARP":
            if self.validate_refractory_period(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_refractory_period(value)

        elif param == "PVARP":
            if self.validate_refractory_period(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_refractory_period(value)

        elif param == "Ventricular Sensitivity":
            if self.validate_sensitivity(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_sensitivity(value)

        elif param == "VRP":
            if self.validate_refractory_period(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_refractory_period(value)

        elif param == "Hysteresis":
            if self.validate_hysteresis(value) == "Valid":
                self.parameter_values[param] = (value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_hysteresis(value)

        elif param == "Rate Smoothing":
            if self.validate_rate_smoothing(value) == "Valid":
                self.parameter_values[param] = int(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.validate_rate_smoothing(value)
        
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
        # Check for validation errors
        validation_errors = self.validate_parameters()

        if validation_errors:
            error_message = "Validation Errors:\n"
            for param, error in validation_errors.items():
                error_message += f"{param}: {error}\n"

            messagebox.showerror("Validation Errors", error_message)
        else:
             # Update parameter_values with the selected pacemaker
            self.parameter_values['Pacemaker'] = self.pacemaker
            self.store_parameter_values()

            # Filter the parameter_values dictionary to include only the parameters for the selected mode
            selected_mode_params = {param: value for param, value in self.parameter_values.items() if param in self.mode_parameters[self.mode_var.get()]}

            print("Parameter values:", selected_mode_params)
            messagebox.showinfo("Success!", "Your data has submitted")
            # You can now use the parameter values as needed

    def validate_parameters(self):
        validation_errors = {}

        # Replace the comments below with the actual validation logic for each parameter
        for param, entry in zip(self.mode_parameters[self.mode_var.get()], self.current_widgets[1::2]):  # Assumes the order of widgets in current_widgets
            value = entry.get()
            error = self.validate_parameter_val(param, value)
            if error != "Valid":
                validation_errors[param] = error

        return validation_errors

    def validate_parameter_val(self, param, value):
        # Validation logic for each parameter
        if param == "Lower Rate Limit":
            return self.validate_lower_rate_limit(value)
        elif param == "Upper Rate Limit":
            return self.validate_upper_rate_limit(value)
        elif param == "Atrial Amplitude" or param == "Ventricular Amplitude":
            return self.validate_amplitude(value)
        elif param == "Atrial Pulse Width" or param == "Ventricular Pulse Width":
            return self.validate_pulse_width(value)
        elif param == "Atrial Sensitivity" or param == "Ventricular Sensitivity":
            return self.validate_sensitivity(value)
        elif param == "ARP" or param == "PVARP" or param == "VRP":
            return self.validate_refractory_period(value)
        elif param == "Hysteresis":
            return self.validate_hysteresis(value)
        elif param == "Rate Smoothing":
            return self.validate_rate_smoothing(value)

        # If no specific validation is found for a parameter, return "Valid" by default
        return "Valid"