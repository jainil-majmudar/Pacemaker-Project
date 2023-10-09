import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image



class SimpleLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pacemaker Interface")
        self.geometry('1100x600')
        self.minsize(1100,600)
        self.resizable(False,False)

        # Create Frames
        bgColor = '#AED2FF'
        self.right_frame = tk.Frame(self, width=350, height=600, bg=bgColor)
        self.right_frame.place(relx=0.7, y=0, relwidth=0.3, relheight=1)
        self.left_frame = tk.Frame(self, width=350, height=600, bg=bgColor)
        self.left_frame.place(x=0, y=0, relwidth=0.3, relheight=1)
        self.login_frame = tk.Frame(self, width=400, height=600, bg=bgColor)
        self.login_frame.place(relx=0.3, y=0, relwidth=0.4, relheight=1)

        # Insert images
        # img=ImageTk.PhotoImage(Image.open("McMaster_logo.png"))
        # image=tk.Label(self.left_frame, image=img,bg=bgColor)

        # Create Labels
        self.heading_label = tk.Label(self.login_frame, text="Pacemaker \nDCM", font=("Inter", 50, "bold"), fg='#00f', bg=bgColor)
        self.heading_label.place(x=45, y=100)
        self.username_label = tk.Label(self.login_frame, text="Username", font=("Inter", 10), fg='#000', bg=bgColor)
        self.username_label.place(x=10, y=300)
        self.username_entry = tk.Entry(self.login_frame, width=46, fg='black', border=2, bg='white')
        self.username_entry.place(x=105, y=300)
        self.password_label = tk.Label(self.login_frame, text="Password", font=("Inter", 10,), fg='#000', bg=bgColor)
        self.password_label.place(x=10, y=350)
        self.password_entry = tk.Entry(self.login_frame, width=46, fg='black', border=2, bg='white')
        self.password_entry.place(x=105, y=350)
        self.login_button = tk.Button(self.login_frame, width=16, border=2, text="Login", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2')
        self.login_button.place(x=105, y=400)
        self.register_button = tk.Button(self.login_frame, width=16, border=2, text="Register", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2',relief='ridge')
        self.register_button.place(x=105, y=460)
        

if __name__ == "__main__":
    app = SimpleLoginApp()
    app.mainloop()