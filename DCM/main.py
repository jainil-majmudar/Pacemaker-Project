import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
import json


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
        self.right_frame.pack(side='right', fill='both', expand=True)
        self.login_frame = tk.Frame(self, width=400, height=600, bg=bgColor)
        self.login_frame.pack(side='right', fill='both', expand=True)
        self.left_frame = tk.Frame(self, width=350, height=600, bg=bgColor)
        self.left_frame.pack(side='left', fill='both', expand=True)
        self.interface = tk.Frame(self,width=1100, height=600,bg='#F5E8B7')
        self.interface.pack(side='left', fill='both', expand=True)
        self.register_frame = tk.Frame(self, width=400, height=600, bg=bgColor)
        self.register_frame.pack(side='left', fill='both', expand=True)
        

        # Load and resize the image
        image = Image.open("DCM/Images/McMaster_logo.png")
        image = image.resize((200, 100))  # Adjust the dimensions as needed
        self.logo_image = ImageTk.PhotoImage(image)

        # Create a Label to display the image
        self.logo_label = tk.Label(self.left_frame, image=self.logo_image, bg=bgColor)
        self.logo_label.pack(side='top', padx=25, pady=10)
        # Create Labels
        #----------- Login Frame---------
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
        self.login_button = tk.Button(self.login_frame, width=16, border=2, text="Login", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=self.login)
        self.login_button.place(x=105, y=400)
        self.register_button = tk.Button(self.login_frame, width=16, border=2, text="Register", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2',relief='ridge', command=self.new_user)
        self.register_button.place(x=105, y=460)

        #-------------Register Frame-----------------
        self.heading_label = tk.Label(self.register_frame, text="Pacemaker \nDCM", font=("Inter", 50, "bold"), fg='#00f', bg=bgColor)
        self.heading_label.place(x=45, y=100)
        self.register_username_label = tk.Label(self.register_frame, text="New Username", font=("Inter", 10), fg='#000', bg=bgColor)
        self.register_username_label.place(x=0, y=300)
        self.register_username_entry = tk.Entry(self.register_frame, width=46, fg='black', border=2, bg='white')
        self.register_username_entry.place(x=115, y=300)
        self.register_password_label = tk.Label(self.register_frame, text="Password", font=("Inter", 10,), fg='#000', bg=bgColor)
        self.register_password_label.place(x=0, y=350)
        self.register_password_label = tk.Label(self.register_frame, text="Confirm Password", font=("Inter", 10,), fg='#000', bg=bgColor)
        self.register_password_label.place(x=0, y=400)
        self.register_password_entry = tk.Entry(self.register_frame, width=46, fg='black', border=2, bg='white')
        self.register_password_entry.place(x=115, y=350)
        self.confirm_password_entry = tk.Entry(self.register_frame, width=46, fg='black', border=2, bg='white')
        self.confirm_password_entry.place(x=115, y=400)
        self.register_button = tk.Button(self.register_frame, width=16, border=2, text="Register", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=self.register)
        self.register_button.place(x=115, y=460)
        self.back_button = tk.Button(self.register_frame, width='16', border = 2, text = "Return Home", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=self.return_home)
        self.back_button.place(x=115, y=520)
        
        #----Interface Frame------
        self.back_button = tk.Button(self.interface, width='16', border = 2, text = "Return Home", font=("Inter", 20, 'bold'), fg='white', bg='black', cursor='hand2', command=self.return_home)
        self.back_button.place(x=115, y=520)
       

        #Following Code Only Shows Login Frame and Lets Login Button Access User Data
        self.load_user_data()
        self.register_frame.pack_forget()
        self.interface.pack_forget()


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for user_data in self.users:
            if username == user_data["username"] and password == user_data["password"]:
                messagebox.showinfo("Login", "Login successful!")
                self.login_frame.pack_forget()
                self.register_frame.pack_forget()
                self.right_frame.pack_forget()
                self.left_frame.pack_forget()
                self.interface.pack()
                return
        messagebox.showerror("Login Error", "Invalid username or password.")



    def new_user(self):
        self.login_frame.pack_forget()
        self.interface.pack_forget()
        self.register_frame.pack()
    
    def return_home(self):
         self.interface.pack_forget()
         self.register_frame.pack_forget()
         self.right_frame.pack(side='right', fill='both', expand=True)
         self.login_frame.pack(side='right', fill='both', expand=True)
         self.left_frame.pack(side='left', fill='both', expand=True)
         
       
       

    def register(self):
        if len(self.users) < 10:
            username = self.register_username_entry.get()
            password = self.register_password_entry.get()
            
            for user_data in self.users:
                if username==user_data['username']:
                    messagebox.showerror("Registration Error", "This username is already in use")
                    return
                else:
                    continue
                    



            if username and password:
                self.users.append({"username": username, "password": password})
                messagebox.showinfo("Registration", "User registered successfully!")
                # Save updated user data to a file
                self.save_user_data()
            else:
                messagebox.showerror("Registration Error", "Username and password are required.")
        else:
            messagebox.showerror("Registration Error", "Maximum 10 users reached.")


    def load_user_data(self):
        try:
            with open("DCM/user_data.json", "r") as file:
                    self.users = json.load(file)
        except FileNotFoundError:
            self.users = []


    def save_user_data(self):
        with open("DCM/user_data.json", "w") as file:
            json.dump(self.users, file)
        
        

if __name__ == "__main__":
    app = SimpleLoginApp()
    app.mainloop()