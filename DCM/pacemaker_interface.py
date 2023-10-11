# pacemaker_interface.py
import tkinter as tk
import json
import tkinter.messagebox as messagebox


class PacemakerInterface:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app

        self.prev_pacemaker = "None"  # Make it an instance variable
        self.previous_pacemaker_label = tk.Label(root, text="Previous Pacemaker Connected: " + "None")
        self.previous_pacemaker_label.place(x=100, y=50)

        # Create and configure the pacemaker interface widgets
        self.pacemaker_label = tk.Label(root, text="Pacemaker To Be Connected To")
        self.pacemaker_label.place(x=100, y=100)
        self.pacemaker_entry = tk.Entry(root, width=46)
        self.pacemaker_entry.place(x=300, y=100)

        self.connection_label = tk.Label(root, text="Communication Established: " + "No")
        self.connection_label.place(x=100,y=500)
        
        self.submit_button = tk.Button(root, text="Submit", command=lambda: self.submit(self.pacemaker_entry.get()))
        self.submit_button.place(x=600, y=100)

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

    def submit(self,entry):
        
        if(self.prev_pacemaker!=entry):
            result = messagebox.askquestion("Note!", "The pacemaker entered is different than the last one connected. Is this okay?")
            if(result == 'yes'):
                self.prev_pacemaker = entry
                self.previous_pacemaker_label.config(text="Previous Pacemaker Connected: " + entry)
                messagebox.showinfo("Note!","Connected successfully")
                self.main.route(self.main.mode_sel)
        else:
            messagebox.showinfo("Note!","Connected successfully")
            self.main.route(self.main.mode_sel)
        
        # # Store the data in the pacemaker_data JSON
        self.pacemaker_data = {
            "pacemaker": entry,
            "mode": 0,
            "upper_rate_limit": 0,
            "lower_rate_limit": 0
        }
        self.save_pacemaker_data()

        

