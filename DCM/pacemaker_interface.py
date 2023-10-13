import tkinter as tk
import json
import tkinter.messagebox as messagebox

class PacemakerInterface:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app

        # Load the previously selected pacemaker from a file
        self.prev_pacemaker = self.load_previous_pacemaker()
        self.previous_pacemaker_label = tk.Label(root, text=f"Previous Pacemaker Connected: {self.prev_pacemaker}", bg='#F5E8B7')
        self.previous_pacemaker_label.place(x=100, y=50)

        # Create and configure the pacemaker interface widgets
        self.pacemaker_label = tk.Label(root, text="Pacemaker To Be Connected To", bg='#F5E8B7')
        self.pacemaker_label.place(x=100, y=100)
        self.pacemaker_entry = tk.Entry(root, width=46)
        self.pacemaker_entry.place(x=300, y=100)

        self.connection_label = tk.Label(root, text="Communication Established: No", bg='#F5E8B7')
        self.connection_label.place(x=100, y=500)

        self.submit_button = tk.Button(root, text="Submit", command=lambda: self.submit(self.pacemaker_entry.get()))
        self.submit_button.place(x=600, y=100)

        self.back_button = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.back_button.place(x=1000, y=20)

        # Place the widgets in the interface
        self.root.pack()

    def load_previous_pacemaker(self):
        try:
            with open("DCM/DataStorage/previous_pacemaker.json", "r") as file:
                data = json.load(file)
                return data.get("previous_pacemaker", "None")
        except FileNotFoundError:
            return "None"

    def save_previous_pacemaker(self, pacemaker):
        data = {"previous_pacemaker": pacemaker}
        with open("DCM/DataStorage/previous_pacemaker.json", "w") as file:
            json.dump(data, file)

    def submit(self, entry):
        if self.prev_pacemaker != entry:
            result = messagebox.askquestion("Note!", "The pacemaker entered is different than the last one connected. Is this okay?")
            if result == 'yes':
                self.prev_pacemaker = entry
                self.previous_pacemaker_label.config(text=f"Previous Pacemaker Connected: {entry}")
                self.save_previous_pacemaker(entry)  # Save the new pacemaker
                messagebox.showinfo("Note!", "Connected successfully")
                self.main.route(self.main.mode_sel)
        else:
            messagebox.showinfo("Note!", "Connected successfully")
            self.main.route(self.main.mode_sel)
