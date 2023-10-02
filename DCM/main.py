import tkinter as tk
import tkinter.messagebox as messagebox

# Dictionary to store user data (name and password)
users = {}

# Maximum number of allowed users
MAX_USERS = 10

class SimpleLoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simple Login App")
        self.geometry("400x300")

        # Create labels
        self.welcome_label = tk.Label(self, text="Welcome to the Simple Login App", font=("Arial", 14))
        self.welcome_label.pack(pady=10)

        # Create login frame
        self.login_frame = tk.Frame(self)

        self.login_label = tk.Label(self.login_frame, text="Login")
        self.login_label.pack(pady=10)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.login_frame.pack_forget()

        # Create registration frame
        self.register_frame = tk.Frame(self)

        self.register_label = tk.Label(self.register_frame, text="Register")
        self.register_label.pack(pady=10)

        self.new_username_label = tk.Label(self.register_frame, text="New Username:")
        self.new_username_label.pack()
        self.new_username_entry = tk.Entry(self.register_frame)
        self.new_username_entry.pack()

        self.new_password_label = tk.Label(self.register_frame, text="New Password:")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.register_frame, show="*")
        self.new_password_entry.pack()

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.pack(pady=10)

        self.register_frame.pack_forget()

        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Login", command=self.show_login_frame)
        file_menu.add_command(label="Register", command=self.show_register_frame)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack()

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if len(users) >= MAX_USERS:
            messagebox.showerror("Registration Failed", "Maximum number of users reached.")
        elif new_username in users:
            messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            users[new_username] = new_password
            messagebox.showinfo("Registration Successful", "User registered successfully.")

if __name__ == "__main__":
    app = SimpleLoginApp()
    app.mainloop()

#hello