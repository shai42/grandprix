import tkinter as tk
from tkinter import messagebox
from models.user import User  # Adjust if your User class is elsewhere
from managers.user_manager import UserManager

def open_register_window(parent_win):
    def register_user():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not (name and email and password and role):
            messagebox.showerror("Error", "All fields are required.")
            return

        new_user = User(name, email, password, role)
        user_manager = UserManager()
        user_manager.register_user(new_user)

        messagebox.showinfo("Success", "Registration successful!")
        register_win.destroy()

    register_win = tk.Toplevel(parent_win)
    register_win.title("Register")
    register_win.geometry("300x200")

    tk.Label(register_win, text="Name:").pack()
    name_entry = tk.Entry(register_win)
    name_entry.pack()

    tk.Label(register_win, text="Email:").pack()
    email_entry = tk.Entry(register_win)
    email_entry.pack()

    tk.Label(register_win, text="Password:").pack()
    password_entry = tk.Entry(register_win, show="*")
    password_entry.pack()

    tk.Label(register_win, text="Role (user/admin):").pack()
    role_var = tk.StringVar(value="user")
    tk.Entry(register_win, textvariable=role_var).pack()

    tk.Button(register_win, text="Register", command=register_user).pack(pady=10)
