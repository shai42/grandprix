"""
Login window for the Grand Prix Experience ticket booking system.
"""
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from models.user import User, Admin
from data.manager import DataManager

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Grand Prix Experience - Login")
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        
        self.data_manager = DataManager()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the login form widgets."""
        # Title
        title_label = tk.Label(self.master, text="Grand Prix Experience", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        # Login Frame
        login_frame = tk.Frame(self.master)
        login_frame.pack(pady=20)
        
        # Email
        tk.Label(login_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = tk.Entry(login_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(login_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Login Button
        login_button = tk.Button(self.master, text="Login", command=self.login, width=15)
        login_button.pack(pady=10)
        
        # Register Button
        register_button = tk.Button(self.master, text="Register", command=self.show_register, width=15)
        register_button.pack(pady=5)
    
    def login(self):
        """Handle login attempt."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        users = self.data_manager.load_users()
        user = None
        
        for u in users:
            if u.get_email() == email and u.get_password() == password:
                user = u
                break
        
        if user:
            self.master.destroy()  # Close login window
            
            # Open appropriate dashboard based on user type
            root = tk.Tk()
            if isinstance(user, Admin):
                from .admin_dashboard import AdminDashboard
                AdminDashboard(root, user)
            else:
                from .ticket_gui import TicketsGUI
                TicketsGUI(root, user)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    
    def show_register(self):
        """Show registration form."""
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("350x250")
        register_window.resizable(False, False)
        
        # Registration Frame
        register_frame = tk.Frame(register_window)
        register_frame.pack(pady=20)
        
        # Name
        tk.Label(register_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(register_frame, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Email
        tk.Label(register_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(register_frame, width=30)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(register_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        password_entry = tk.Entry(register_frame, width=30, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Register Button
        def register():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            
            if not name or not email or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            users = self.data_manager.load_users()
            
            # Check if email already exists
            if any(u.get_email() == email for u in users):
                messagebox.showerror("Error", "Email already registered")
                return
            
            # Create new user
            new_user = User(
                user_id=len(users) + 1,
                name=name,
                email=email,
                password=password
            )
            
            users.append(new_user)
            self.data_manager.save_users(users)
            
            messagebox.showinfo("Success", "Registration successful! Please login.")
            register_window.destroy()
        
        register_button = tk.Button(register_window, text="Register", command=register, width=15)
        register_button.pack(pady=10) 