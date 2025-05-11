import tkinter as tk
from tkinter import messagebox
from managers.user_manager import UserManager
from gui.user_dashboard import open_user_dashboard
from gui.admin_dashboard import open_admin_dashboard

user_manager = UserManager()

def login_window():
    def attempt_login():
        email = email_entry.get()
        password = password_entry.get()
        user = user_manager.login(email, password)
        if user:
            login_win.destroy()
            if user.getRole().lower() == "admin":
                open_admin_dashboard(user)
            else:
                open_user_dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    login_win = tk.Tk()
    login_win.title("Grand Prix Booking - Login")
    login_win.geometry("300x150")

    tk.Label(login_win, text="Email:").pack()
    email_entry = tk.Entry(login_win)
    email_entry.pack()

    tk.Label(login_win, text="Password:").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    tk.Button(login_win, text="Login", command=attempt_login).pack(pady=10)

    login_win.mainloop()
