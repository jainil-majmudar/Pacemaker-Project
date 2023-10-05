import tkinter as tk
import tkinter.messagebox as messagebox



class SimpleLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pacemaker Interface")
        self.geometry("1100x600")

        # Create labels
        self.welcome_label = tk.Label(self, text="Welcome!", font=("Inter 1000", 50, "bold"), fg='#00f')
        self.welcome_label.pack(pady=50)

        # Creating grid
        self.grid()




if __name__ == "__main__":
    app = SimpleLoginApp()
    app.mainloop()