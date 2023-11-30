import tkinter as tk
from user_manager import UserManager
from pacemaker_interface import PacemakerInterface
from mode_sel import ModeSel
from egram import Egram
from display import Display
from PIL import ImageTk, Image
from serial_communication import SerialCommunication


class SimpleLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pacemaker Interface")
        self.geometry('1100x600')
        self.resizable(False,False)
        self.username = ""
        self.pacemaker_port = ""
        self.heart_port = ""
        self.login_bool = True
        self.port_list = ["",""]
        self.bgcolor2 = "#C5FFF8"

        # Create Frames
        bgColor = '#AED2FF'
      
        self.login_frame = tk.Frame(self, width=1100, height=600, bg=bgColor)
        self.login_frame.pack(side='right', fill='both', expand=True)
       
        self.pacemaker_sel = tk.Frame(self, width=1100, height=600, bg=self.bgcolor2)
        
        self.mode_sel = tk.Frame(self, width=1100, height=600, bg=self.bgcolor2)

        self.register_frame = tk.Frame(self, width=1100, height=600, bg=bgColor)

        self.display_frame = tk.Frame(self, width=1100, height=600, bg=self.bgcolor2)
        self.no_data_frame = tk.Frame(self, width=1100, height=600, bg=self.bgcolor2)

        self.egram_frame = tk.Frame(self, width=1100, height=600, bg=self.bgcolor2)

        
        

        # Load and resize the image
        image = Image.open("DCM/Images/McMaster_logo.png")
        image = image.resize((200, 100))  # Adjust the dimensions as needed
        self.logo_image = ImageTk.PhotoImage(image)

        # Create a Label to display the image
        self.logo_label = tk.Label(self.login_frame, image=self.logo_image, bg=bgColor)
        self.logo_label.place(x=25, y=10)
        self.logo_label2 = tk.Label(self.register_frame, image=self.logo_image, bg=bgColor)
        self.logo_label2.place(x=25, y=10)

        # Login Frame
        self.heading_label = tk.Label(self.login_frame, text="Pacemaker \nDCM", font=("Inter", 50, "bold"), fg='#00f', bg=bgColor)
        self.heading_label.place(x=410, y=100)
        self.username_label = tk.Label(self.login_frame, text="Username", font=("Inter", 10), fg='#000', bg=bgColor)
        self.username_label.place(x=365, y=300)
        self.username_entry = tk.Entry(self.login_frame, width=46, fg='black', border=2, bg='white')
        self.username_entry.place(x=465, y=300)
        self.password_label = tk.Label(self.login_frame, text="Password", font=("Inter", 10), fg='#000', bg=bgColor)
        self.password_label.place(x=365, y=350)
        self.password_entry = tk.Entry(self.login_frame, show="*", width=46, fg='black', border=2, bg='white')
        self.password_entry.place(x=465, y=350)
        self.login_button = tk.Button(self.login_frame, width=16, border=2, text="Login", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=self.login)
        self.login_button.place(x=465, y=400)
        self.register_button = tk.Button(self.login_frame, width=16, border=2, text="Register", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2',relief='ridge', command=lambda: self.route(self.register_frame))
        self.register_button.place(x=465, y=460)

        # Register Frame
        self.heading_label = tk.Label(self.register_frame, text="Pacemaker \nDCM", font=("Inter", 50, "bold"), fg='#00f', bg=bgColor)
        self.heading_label.place(x=410, y=100)
        self.register_username_label = tk.Label(self.register_frame, text="New Username", font=("Inter", 10), fg='#000', bg=bgColor)
        self.register_username_label.place(x=350, y=300)
        self.register_username_entry = tk.Entry(self.register_frame, width=46, fg='black', border=2, bg='white')
        self.register_username_entry.place(x=465, y=300)
        self.register_password_label = tk.Label(self.register_frame, text="Password", font=("Inter", 10), fg='#000', bg=bgColor)
        self.register_password_label.place(x=350, y=350)
        self.register_password_label = tk.Label(self.register_frame, text="Confirm Password", font=("Inter", 10), fg='#000', bg=bgColor)
        self.register_password_label.place(x=350, y=400)
        self.register_password_entry = tk.Entry(self.register_frame, show="*", width=46, fg='black', border=2, bg='white')
        self.register_password_entry.place(x=465, y=350)
        self.confirm_password_entry = tk.Entry(self.register_frame, show="*", width=46, fg='black', border=2, bg='white')
        self.confirm_password_entry.place(x=465, y=400)
        self.register_button2 = tk.Button(self.register_frame, width=16, border=2, text="Register", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=self.register)
        self.register_button2.place(x=465, y=460)
        self.back_button = tk.Button(self.register_frame, width='16', border = 2, text = "Return Home", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=lambda: self.route(self.login_frame))
        self.back_button.place(x=465, y=520)

        

    def login(self):
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        self.password_entry.delete(0,'end')
        self.username_entry.delete(0,'end')
        pacemaker_interface.update_prev_pacemaker_label()
        user_manager.login_user(self.username,password)
    
    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm = self.confirm_password_entry.get()
        self.confirm_password_entry.delete(0,'end')
        self.register_password_entry.delete(0,'end')
        self.register_username_entry.delete(0,'end')
        user_manager.register_user(username,password,confirm)
        


    def route(self, target_frame):
        if target_frame == self.login_frame:
            self.login_bool = True
        # Hide the current frame and show the target frame
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.pacemaker_sel.pack_forget()
        self.mode_sel.pack_forget()
        self.display_frame.pack_forget()
        self.no_data_frame.pack_forget()
        self.egram_frame.pack_forget()
        self.confirm_password_entry.delete(0,'end')
        self.register_password_entry.delete(0,'end')
        self.register_username_entry.delete(0,'end')
        self.password_entry.delete(0,'end')
        self.username_entry.delete(0,'end')
        target_frame.pack()

if __name__ == "__main__":
    app = SimpleLoginApp()
    user_manager = UserManager("DCM/DataStorage/user_data.json", app)
    pacemaker_interface = PacemakerInterface(app.pacemaker_sel, app)
    mode_selection = ModeSel(app.mode_sel,app)
    display_data = Display(app.display_frame,app.no_data_frame, app)
    egram_data = Egram(app.egram_frame,app)
    serial_comm = SerialCommunication(app)
    app.mode_selection = mode_selection
    app.pacemaker_interface = pacemaker_interface
    app.user_manager = user_manager  # Set the UserManager instance in your main app
    app.display_data = display_data
    app.egram_data = egram_data
    app.serial_comm = serial_comm
    app.mainloop()
