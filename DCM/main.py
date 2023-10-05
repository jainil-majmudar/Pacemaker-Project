import tkinter as tk
import tkinter.messagebox as messagebox



class SimpleLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pacemaker Interface")
        self.geometry("600x600")

        # Create labels
        self.welcome_label = tk.Label(self, text="Welcome!", font=("Arial", 14))
        self.welcome_label.pack(pady=10)




if __name__ == "__main__":
    app = SimpleLoginApp()
    app.mainloop()