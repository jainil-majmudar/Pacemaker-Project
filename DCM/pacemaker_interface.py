# pacemaker_interface.py
import tkinter as tk
import json

class PacemakerInterface:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app

        # Create and configure the pacemaker interface widgets
        self.pacemaker_label = tk.Label(root, text="Pacemaker To Be Connected To")
        self.pacemaker_label.place(x=100, y=100)
        self.pacemaker_entry = tk.Entry(root, width=46)
        self.pacemaker_entry.place(x=300, y=100)
        self.mode_label = tk.Label(root, text="Select Mode")
        self.mode_label.place(x=100, y=230)
        self.mode_var = tk.StringVar()
        modes = ["AOO", "VOO", "AAI", "VVI"]
        mode_dropdown = tk.OptionMenu(root, self.mode_var, *modes)
        mode_dropdown.place(x=200, y=230)

        # Parameters
        self.upper_rate_label = tk.Label(root, text="Upper Rate Limit")
        self.upper_rate_label.place(x=100, y=400)
        self.upper_rate_entry = tk.Entry(root, width=10)
        self.upper_rate_entry.place(x=250, y=400)

        self.lower_rate_label = tk.Label(root, text="Lower Rate Limit")
        self.lower_rate_label.place(x=100, y=500)
        self.lower_rate_entry = tk.Entry(root, width=10)
        self.lower_rate_entry.place(x=250, y=500)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.place(x=400, y=550)

        self.back_button = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.back_button.place(x=1000, y=20)

        # Load and initialize pacemaker data
        self.pacemaker_data = {}
        self.load_pacemaker_data()

        # Place the widgets in the interface
        self.root.pack()

    def load_pacemaker_data(self):
        try:
            with open("DCM/DataStorage/pacemaker_data.json", "r") as file:
                self.pacemaker_data = json.load(file)
        except FileNotFoundError:
            self.pacemaker_data = {}

    def save_pacemaker_data(self):
        with open("DCM/DataStorage/pacemaker_data.json", "w") as file:
            json.dump(self.pacemaker_data, file)

    def submit(self):
        pacemaker_name = self.pacemaker_entry.get()
        mode = self.mode_var.get()
        upper_rate_limit = self.upper_rate_entry.get()
        lower_rate_limit = self.lower_rate_entry.get()

        # Store the data in the pacemaker_data JSON
        self.pacemaker_data = {
            "pacemaker": pacemaker_name,
            "mode": mode,
            "upper_rate_limit": upper_rate_limit,
            "lower_rate_limit": lower_rate_limit
        }
        self.save_pacemaker_data()

        # Handle pacemaker interface actions here, e.g., connecting to the pacemaker
        print("Pacemaker Data Saved")