import tkinter as tk
import json
import tkinter.messagebox as messagebox
from serial_communication import SerialCommunication  # Import your serial_communication module


class PacemakerInterface:
    def __init__(self, root, main_app):
        self.root = root
        self.main = main_app
        self.serial_comm = SerialCommunication(self.main)


        self.connection_label = tk.Label(root, text="Communication Established: No", font=("Inter", 10, 'bold'), fg='black', bg=self.main.bgcolor2)
        self.connection_label.place(x=100, y=500)

        self.previous_pacemaker_label = tk.Label(self.root, text="",  font=("Inter", 10, 'bold'), fg='black', bg=self.main.bgcolor2)

        self.previous_pacemaker_label = tk.Label(self.root, text=f"Previous Pacemaker Connected: ",  font=("Inter", 10, 'bold'), fg='black', bg=self.main.bgcolor2)
        self.previous_pacemaker_label.place(x=100, y=50)


        # Create and configure the pacemaker interface widgets
        self.pacemaker_label = tk.Label(root, text="Insert name for Pacemaker", font=("Inter", 10, 'bold'), fg='black', bg=self.main.bgcolor2)
        self.pacemaker_label.place(x=100, y=100)
        self.pacemaker_entry = tk.Entry(root, width=46)
        self.pacemaker_entry.place(x=325, y=100)

        self.submit_button = tk.Button(root, text="Submit", font=("Inter", 10, 'bold'), fg='white', bg='green', cursor='hand2', command=lambda: self.submit(self.pacemaker_entry.get()))
        self.submit_button.place(x=625, y=100)

        self.log_out = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=lambda: self.main.route(self.main.login_frame))
        self.log_out.place(x=1000, y=30)

        # Place the widgets in the interface
        self.root.pack()

    def load_previous_pacemaker(self):
        username = self.main.username
        try:
            with open("DCM/DataStorage/previous_pacemaker.json", "r") as file:
                data = json.load(file)
                if username in data:
                    key = data[username]
                    return key
        except FileNotFoundError:
            return "None"

    def save_previous_pacemaker(self, pacemaker):
        username = self.main.username
        try:
            with open("DCM/DataStorage/previous_pacemaker.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return "None"
        data[username] = pacemaker

        with open("DCM/DataStorage/previous_pacemaker.json", "w") as file:
            json.dump(data, file)

    def update_prev_pacemaker_label(self):
        self.previous_pacemaker_label.destroy()
        self.previous_pacemaker_label = tk.Label(self.root, text=f"Previous Pacemaker Connected: {self.load_previous_pacemaker()}",  font=("Inter", 10, 'bold'), fg='black', bg=self.main.bgcolor2)
        self.previous_pacemaker_label.place(x=100, y=50)
    
    def update_connection_label(self):
        connected = self.serial_comm.check_connection()
        
        if connected:
            self.connection_label.config(text="Communication Established: Yes", fg='green')
        else:
            self.connection_label.config(text="Communication Established: No", fg='red')

    def check_and_update_connection(self):
        if self.main.login_bool == False:
            self.update_connection_label()  # Update the connection label
            # Schedule to check and update again after 2 seconds
            self.root.after(100, self.check_and_update_connection)
    

    def submit(self, entry):
        if not self.serial_comm.check_connection():
            return messagebox.showerror("Error", "Please connect your pacemaker or check your pacemaker connection")
        elif entry.isspace():
            return messagebox.showerror("Error", "Please enter your Pacemaker")
        elif entry == "":
            return messagebox.showerror("Error", "Please enter your Pacemaker")
        elif self.load_previous_pacemaker() != entry:
            result = messagebox.askquestion("Note!", "The pacemaker entered is different than the last one connected. Is this okay?")
            if result == 'yes':
                self.save_previous_pacemaker(entry)  # Save the new pacemaker
                messagebox.showinfo("Note!", "Connected successfully")
                self.main.mode_selection.reset_mode_sel()
                self.main.route(self.main.mode_sel)
                
        else:
            messagebox.showinfo("Note!", "Connected successfully")
            self.main.route(self.main.mode_sel)
