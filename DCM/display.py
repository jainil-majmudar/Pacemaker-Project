import tkinter as tk
from tkinter import ttk
import json
import tkinter.messagebox as messagebox

class Display(tk.Tk):
    def __init__(self, root, root2, main_app):
        self.root = root
        self.root2 = root2
        self.main = main_app
        self.pacemaker_list = []
        self.selected_pacemaker = tk.StringVar(root)

        self.label4 = tk.Label(root2, text="No Existing Data Found for this user", font=("Inter", 20, 'bold'), fg='red', bg='#F5E8B7')
        self.label4.place(x=300, y=250)
        self.current_display = []

        
        # Create a label to display parameters
        self.label1 = tk.Label(root, text="Please Choose a Pacemaker in order to view past data", font=("Inter", 10, 'bold'), fg='black', bg='#F5E8B7')
        self.label1.place(x=100, y=30)
        self.label2 = tk.Label(root, text="Your data will appear below :", font=("Inter", 10, 'bold'), fg='black', bg='#F5E8B7')
        self.label2.place(x=100, y=150)
        self.label3 = tk.Label(root, text="", font=("Inter", 10), fg='black', bg='#F5E8B7')
        self.label3.place(x=100, y=200)
        self.label3.config(wraplength=1000)
        # Create a button to display parameters
        self.display_button = tk.Button(root, text="Display", font=("Inter", 10, 'bold'), fg='white', bg='green', cursor='hand2', command=self.display_parameters)
        self.display_button.place(x=200, y=60)

        log_out = tk.Button(root, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=self.log_out)
        log_out.place(x=1000, y=30)
        back_button = tk.Button(root, text="Back", width='10', border=2, font=("Inter", 10, 'bold'), fg='white', bg='black', cursor='hand2', command=self.back_button)
        back_button.place(x=900, y=30)
        log_out = tk.Button(root2, width='10', border=2, text="Log Out", font=("Inter", 10, 'bold'), fg='white', bg='red', cursor='hand2', command=self.log_out)
        log_out.place(x=1000, y=30)
        back_button = tk.Button(root2, text="Back", width='10', border=2, font=("Inter", 10, 'bold'), fg='white', bg='black', cursor='hand2', command=self.back_button)
        back_button.place(x=900, y=30)

        self.canvas = tk.Canvas(root, bg='#F5E8B7', width=900, height=400, scrollregion=(0, 0, 1000, 400))
        self.canvas.place(x=100, y=200)
        self.scroll_frame = tk.Frame(self.canvas, bg='#F5E8B7')
        self.scroll_frame.place(relx=0, rely=0, anchor='nw')
        self.scrollbar = ttk.Scrollbar(root, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.place(x=100, y=580, width=900)
        self.canvas.config(xscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.scroll_frame.bind('<Configure>', self.on_frame_configure)
        

    def on_frame_configure(self,event):
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    
    def back_button(self):
        self.main.route(self.main.mode_sel)
        self.selected_pacemaker.set("")
        for label in self.current_display:
            label.destroy()
        self.main.mode_selection.reset_mode_sel

    def log_out(self):
        self.main.route(self.main.login_frame)
        self.selected_pacemaker.set("")
        for label in self.current_display:
            label.destroy()
        self.main.mode_selection.reset_mode_sel

    def display(self):
        self.main.route(self.main.display_frame)
        self.pacemaker_list = self.load_existing_pacemakers()
        # Create a dropdown menu to select an existing pacemaker
        if self.pacemaker_list == []:
            self.root2.pack()
            self.root.pack_forget()
            return
        else:
            self.root2.pack_forget()
            self.root.pack()
            self.pacemaker_dropdown = tk.OptionMenu(self.root, self.selected_pacemaker, *self.pacemaker_list)
            self.pacemaker_dropdown.config(bg="blue", fg="white")
            self.pacemaker_dropdown["menu"].config(bg="blue", fg = 'white')
            self.pacemaker_dropdown.place(x=100,y=60)
            return
            



            

    def load_existing_pacemakers(self):
        username = self.main.username
        # Load existing pacemakers from pacemaker_data.json
        try:
            with open("DCM/DataStorage/pacemaker_data.json", "r") as file:
                json_data = json.load(file)
            # Get the list of pacemakers from the JSON data

            if username in json_data:
                user_pacemakers = json_data[username]
                pacemakers = list(user_pacemakers.keys())
                return pacemakers
            else:
                return []
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Return an empty list if there's an issue with the JSON file
            return []

    def display_parameters(self):
        username = self.main.username
        # Get the selected pacemaker
        selected_pacemaker = self.selected_pacemaker.get()
        if not selected_pacemaker:
            return  # No pacemaker selected

        # Load existing pacemakers from pacemaker_data.json
        try:
            with open("DCM/DataStorage/pacemaker_data.json", "r") as file:
                json_data = json.load(file)
            # Get the parameters for the selected pacemaker
            if username in json_data:
                user_pacemakers = json_data[username]
                parameters = user_pacemakers.get(selected_pacemaker, {})
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            parameters = {}  # Set parameters as an empty dictionary if there's an issue with the JSON file

        column = 50  
        for display in self.current_display:
            display.destroy()
        self.current_display = []
        for mode, params in parameters.items():
            label_mode = tk.Label(self.scroll_frame, justify="left", text=mode, bg="#F5E8B7")
            label_mode.grid(row=0, sticky='W', column=column, padx=10)

            row = 1 
            for param, value in params.items():
                label_param = tk.Label(self.scroll_frame, justify="left", text=param, bg="#F5E8B7")
                label_param.grid(row=row, sticky='W', column=column, padx=10)

                label_value = tk.Label(self.scroll_frame, text=value, justify="left", bg="#F5E8B7")
                label_value.grid(row=row, sticky='W', column=column + 1, padx=10)

                row += 1
                self.current_display.extend([label_mode, label_param, label_value])

            column += 2
