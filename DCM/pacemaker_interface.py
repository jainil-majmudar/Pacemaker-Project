# pacemaker_interface.py
import tkinter as tk

class PacemakerInterface:
    def __init__(self, root):
        self.root = root

        # Create and configure the pacemaker interface widgets
        self.pacemaker_label = tk.Label(root, text="Pacemaker To Be Connected To")
        self.pacemaker_label.place(x=100,y=500)
        self.pacemaker_entry = tk.Entry(root, width=46)
        self.pacemaker_entry.place(x=200,y=500)
        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.place(x=400,y=500)

        # Place the widgets in the interface
        self.root.pack()
       
        

    def submit(self):
        pacemaker_name = self.pacemaker_entry.get()
        # Handle pacemaker interface actions here, e.g., connecting to the pacemaker
        print(f"Connecting to pacemaker: {pacemaker_name}")
        # Add your pacemaker interaction code here
