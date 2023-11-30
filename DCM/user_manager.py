# user_manager.py
import json
import tkinter as tk
import tkinter.messagebox as messagebox
from serial_communication import SerialCommunication  # Import your serial_communication module

class UserManager:
    def __init__(self, user_data_file, main_app):
        self.user_data_file = user_data_file
        self.users = self.load_user_data()
        self.main = main_app
        self.serial_comm = SerialCommunication(self.main)

    def load_user_data(self):
        try:
            with open(self.user_data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_user_data(self):
        with open(self.user_data_file, "w") as file:
            json.dump(self.users, file)

    def register_user(self, username, password, confirm):
        if len(self.users) >= 10:
            return messagebox.showerror("Registration Error", "Maximum 10 users reached.")

        for user_data in self.users:
            if username == user_data['username']:
                return messagebox.showerror("Registration Error", "This username is already in use")

        if username and password:
            if(password == confirm):
                self.users.append({"username": username, "password": password})
                self.save_user_data()
                return messagebox.showinfo("Registration", "User registered successfully!")
            else:
                return messagebox.showerror("Registration Error", "Passwords don't match!")
        else:
            return messagebox.showerror("Registration Error", "Username and password are required.")

    def login_user(self, username, password):
        for user_data in self.users:
            if username == user_data["username"] and password == user_data["password"]:
                self.main.login_bool = False
                self.main.port_list = ["", ""]
                self.main.route(self.main.pacemaker_sel)
                self.main.pacemaker_interface.check_and_update_connection()
                return messagebox.showinfo("Login", "Login successful!")

        return messagebox.showerror("Login Error", "Invalid username or password.")
