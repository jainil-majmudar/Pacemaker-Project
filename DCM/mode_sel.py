import tkinter as tk
import json
import tkinter.messagebox as messagebox
from itertools import zip_longest

class ModeSel:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app
        self.error_labels = {}

        self.mode_label = tk.Label(root, font=("Inter", 10, 'bold'), fg='black', bg='#F5E8B7', cursor='hand2',text="Select Mode")
        self.mode_label.place(x=100, y=30)
        self.mode_var = tk.StringVar()
        self.current_mode = ""
        self.modes = ["AOO", "VOO", "AAI", "VVI", "AOOR", "VOOR", "AAIR", "VVIR"]
        self.mode_dropdown = tk.OptionMenu(root, self.mode_var, *self.modes)
        self.mode_dropdown.config(bg="blue", fg="white")
        self.mode_dropdown["menu"].config(bg="blue", fg = 'white')
        self.mode_dropdown.place(x=100, y=60)
        next_button = tk.Button(root, text="Next", font=("Inter", 10, 'bold'), fg='white', bg='blue', cursor='hand2', command=lambda: self.render(self.mode_var.get()))
        next_button.place(x=200, y=60)

        display_data_button = tk.Button(root, text = "Display Existing Data", font=("Inter", 10, 'bold'), fg='white', bg='green', cursor='hand2', command=lambda :self.display())
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
            "VVI": ["Lower Rate Limit", "Upper Rate Limit", "Ventricular Amplitude", "Ventricular Pulse Width", "Ventricular Sensitivity", "VRP", "Hysteresis", "Rate Smoothing"],
            "AOOR": ["Lower Rate Limit", "Upper Rate Limit", "Maximum Sensor Rate", "Atrial Amplitude", "Atrial Pulse Width", "Activity Threshold", "Reaction Time", "Response Factor", "Recovery Time"],
            "VOOR": ["Lower Rate Limit", "Upper Rate Limit", "Maximum Sensor Rate", "Ventricular Amplitude", "Ventricular Pulse Width", "Activity Threshold", "Reaction Time", "Response Factor", "Recovery Time"],
            "AAIR": ["Lower Rate Limit", "Upper Rate Limit", "Maximum Sensor Rate", "Atrial Amplitude", "Atrial Pulse Width", "Atrial Sensitivity", "ARP", "PVARP", "Hysteresis", "Rate Smoothing", "Activity Threshold", "Reaction Time", "Response Factor", "Recovery Time"],
            "VVIR": ["Lower Rate Limit", "Upper Rate Limit", "Maximum Sensor Rate", "Ventricular Amplitude", "Ventricular Pulse Width", "Ventricular Sensitivity", "VRP", "Hysteresis", "Rate Smoothing", "Activity Threshold", "Reaction Time", "Response Factor", "Recovery Time"]
        }

        self.current_widgets = []  # To store current widgets for mode parameters
        self.current_vals = []
        self.current_param_vals = []
        self.current_mode = ""

        # Initialize the parameter values dictionary with default values
        self.parameter_values = {
            "Lower Rate Limit": 60,
            "Upper Rate Limit": 120,
            "Maximum Sensor Rate": 120,
            "Atrial Amplitude": 5,
            "Atrial Pulse Width": 1,
            "Atrial Sensitivity": "",
            "Ventricular Amplitude": 5,
            "Ventricular Pulse Width": 1,
            "Ventricular Sensitivity": "",
            "ARP": 250,
            "VRP": 320,
            "PVARP": 250,
            "Hysteresis":0,
            "Rate Smoothing": 0,
            "Activity Threshold": "med",
            "Reaction Time": 30,
            "Response Factor": 8,
            "Recovery Time": 5
        }

    def display(self):
        self.main.display_data.display()

    def render(self, mode):
        self.current_mode = self.mode_var.get()
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
                        return "Lower Rate Limit should be an integer between 50ppm and 90ppm."
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
        
    def maximum_sensor_rate(self, value):
        try:
            value = float(value)
            if 50 <= value <= 175:
                if value % 5 == 0:
                    return "Valid"
                else:
                    return "Maximum Sensor Rate should be a multiple of 5 between 50ppm and 175ppm."
            else:
                return "Maximum Sensor Rate should be between 50ppm and 175ppm."
        except ValueError:
            return "Maximum Sensor Rate should be a valid value."
     
    def validate_amplitude(self, value):
        try:
            value = float(value)
            if value==0:
                return "Valid"
            elif 0.1<=value<=5.0:
                list = []
                temp = 0.1
                while temp <= 5.1:
                    list.append(round(temp,1))
                    temp+=0.1
                if value in list:
                    return "Valid"
                else:
                    return "Amplitude should be a multiple of 0.1 if between 0.1V and 5.0V."
            else:
                return "Amplitude should be 0V or between 0.1V - 5.0V"
        except ValueError:
            return "Amplitude should be a valid value."
        
    def validate_pulse_width(self, value):
        try:
            value = float(value)
            if 1 <= value <= 30:
                if value.is_integer():
                    return "Valid"
                else:
                    return "Pulse Width should be an integer between 1ms and 30ms."
            else:
                return "Pulse Width should be a multiple of 1 between 1ms and 30ms"
        except ValueError:
            return "Pulse Width should be a valid value."

    def validate_sensitivity(self, value):
        try:
            value = float(value)
            if 0<=value<=5:
                list = []
                temp = 0
                while temp <= 5.1:
                    list.append(round(temp,1))
                    temp+=0.1
                if value in list:
                    return "Valid"
                else:
                    return "Sensitivity should be a multiple of 0.1 if between 0V and 5V."
            else:
                return "Amplitude should be between 0V - 5V"
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
            if value==0 or 30 <= value <= 175:
                if value==0:
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
                return "Hysteresis should be 0ppm or between 30ppm and 175ppm."
        except ValueError:
            return "Hysteresis should be a valid value."
        
    def validate_rate_smoothing(self, value):
        try:
            value = int(value)
            if 0 <= value <= 21:
                if value % 3 == 0:
                    return "Valid"
                else:
                    return "Rate Smoothing should be one of these values-> 0%, 3%, 6%, 9%, 12%, 15%, 18%, 21%"
            elif value == 25:
                return "Valid"
            else:
                return "Rate Smoothing should be one of these values-> 0%, 3%, 6%, 9%, 12%, 15%, 18%, 21%, 25%"
        except ValueError:
            return "Rate smoothing should be a valid percentage."
        
    def activity_threshold(self, value):
        try:
            value_lower = value.lower()
            if value_lower == "v-low" or value_lower == "low" or value_lower == "med-low" or value_lower == "med" or value_lower == "med-high" or value_lower == "high" or value_lower == "v-high":
                return "Valid"
            else:
                return "Activity Threshold needs to be v-low, low, med-low, med, med-high, high or v-high"
        except ValueError:
            return "Activity Threshold needs to be v-low, low, med-low, med, med-high, high or v-high"
        
    def reaction_time(self, value):
        try:
            value = float(value)
            if 10 <= value <= 50:
                if value % 10 == 0:
                    return "Valid"
                else:
                    return "Reaction Time should be a multiple of 10 between 10sec and 50sec."
            else:
                return "Reaction Time should be between 10sec and 50sec."
        except ValueError:
            return "Reaction Time should be a valid value."
        
    def response_factor(self, value):
        try:
            value = float(value)
            if 1 <= value <= 16:
                if value.is_integer():
                    return "Valid"
                else:
                    return "Response Factor should be an integer between 1 and 16."
            else:
                return "Response Factor should be a multiple of 1 between 1 and 16"
        except ValueError:
            return "Response Factor should be a valid value."
        
    def recovery_time(self, value):
        try:
            value = float(value)
            if 2 <= value <= 16:
                if value.is_integer():
                    return "Valid"
                else:
                    return "Recovery Time should be an integer between 2min and 16min."
            else:
                return "Recovery Time should be a multiple of 1min between 2min and 16min"
        except ValueError:
            return "Recovery Time should be a valid value."

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
        
        elif param == "Maximum Sensor Rate":
            if self.maximum_sensor_rate(value) == "Valid":
                self.parameter_values[param] = float(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.maximum_sensor_rate(value)

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

        elif param == "Activity Threshold":
            if self.activity_threshold(value) == "Valid":
                self.parameter_values[param] = value
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.activity_threshold(value)

        elif param == "Reaction Time":
            if self.reaction_time(value) == "Valid":
                self.parameter_values[param] = int(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.reaction_time(value)

        elif param == "Response Factor":
            if self.response_factor(value) == "Valid":
                self.parameter_values[param] = int(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.response_factor(value)

        elif param == "Recovery Time":
            if self.recovery_time(value) == "Valid":
                self.parameter_values[param] = int(value)
                self.error_labels[param]["text"] = ""  # Clear the error message
            else:
                self.error_labels[param]["text"] = self.recovery_time(value)
        
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
                try:
                    json_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    # Handle the case of an empty JSON file
                    json_data = {}
        except FileNotFoundError:
            json_data = {}
        if not json_data:
            json_data = {}

        # Get the selected pacemaker and mode
        selected_pacemaker = self.parameter_values['Pacemaker']
        selected_mode = self.current_mode

        username = self.main.username  # Assuming the user module has a username variable
        
        print(f"\n--------------------------------\nStored parameter values for the user '{username}' on the '{selected_pacemaker}' pacemaker, for the selected mode '{selected_mode}'.")

        # Filter the parameter_values dictionary to include only the parameters for the selected mode
        selected_mode_params = {param: value for param, value in self.current_param_vals if param in self.mode_parameters[selected_mode]}
        
        # Check if there is an entry for the selected pacemaker
        
        if username in json_data:
            if selected_pacemaker in json_data[username]:
                # Update the existing entry with the new parameter values
                json_data[username][selected_pacemaker][selected_mode] = selected_mode_params
            else:
                # Create a new entry for the selected pacemaker
                json_data[username][selected_pacemaker] = {selected_mode: selected_mode_params}
        else:
            # Create a new entry for the username and pacemaker
            json_data[username] = {selected_pacemaker: {selected_mode: selected_mode_params}}

        # Save the updated JSON data back to the file
        with open("DCM/DataStorage/pacemaker_data.json", "w") as file:
            json.dump(json_data, file)


        

    def show_parameter_values(self):
        if self.current_mode!=self.mode_var.get():
            messagebox.showerror("Error", "Please press next to render before submitting")
            return
        for widget in self.current_widgets[1::2]:
            val = widget.get()
            self.current_vals.append(val)
        self.current_param_vals = list(zip_longest(self.mode_parameters[self.current_mode], self.current_vals))

        # Check for validation errors
        validation_errors = self.validate_parameters()
        if validation_errors:

            error_message = "Validation Errors:\n"
            for param, error in validation_errors.items():
                error_message += f"{param}: {error}\n"

            messagebox.showerror("Validation Errors", error_message)
            self.current_vals = []

        else:
             # Update parameter_values with the selected pacemaker
            self.store_parameter_values()
            self.parameter_values['Pacemaker'] = self.pacemaker
            

            
            # Filter the parameter_values dictionary to include only the parameters for the selected mode
            # selected_mode_params = {param: value for param, value in self.current_param_vals if param in self.mode_parameters[self.mode_var.get()]}
            print("--------Parameter values--------")
            i=0
            for param in self.mode_parameters[self.current_mode]:
                print(param, ":", self.current_vals[i])
                i+=1
            messagebox.showinfo("Success!", "Your data has submitted")
            self.current_vals = []
            # You can now use the parameter values as needed

        

    def validate_parameters(self):
        validation_errors = {}
        # Replace the comments below with the actual validation logic for each parameter
        for param, val in self.current_param_vals:  # Assumes the order of widgets in current_widgets
            error = self.validate_parameter_val(param, val)
            if error != "Valid":
                validation_errors[param] = error
        return validation_errors

    def validate_parameter_val(self, param, value):
        # Validation logic for each parameter
        if param == "Lower Rate Limit":
            return self.validate_lower_rate_limit(value)
        elif param == "Upper Rate Limit":
            return self.validate_upper_rate_limit(value)
        if param == "Maximum Sensor Rate":
            return self.maximum_sensor_rate(value)
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
        elif param == "Activity Threshold":
            return self.activity_threshold(value)
        elif param == "Reaction Time":
            return self.reaction_time(value)
        elif param == "Response Factor":
            return self.response_factor(value)
        elif param == "Recovery Time":
            return self.recovery_time(value)

        # If no specific validation is found for a parameter, return "Valid" by default
        return "Valid"