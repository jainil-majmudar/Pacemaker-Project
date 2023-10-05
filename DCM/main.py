import tkinter as tk
import tkinter.messagebox as messagebox



class SimpleLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pacemaker Interface")
        self.geometry("600x600")

        # Create labels
        self.welcome_label = tk.Label(self, text="Welcome!", font=("Times New Roman", 50), fg='#f00')
        self.welcome_label.pack(pady=50)




if __name__ == "__main__":
    app = SimpleLoginApp()
    app.mainloop()