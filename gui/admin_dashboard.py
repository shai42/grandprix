import tkinter as tk

def open_admin_dashboard(admin):
    win = tk.Tk()
    win.title(f"Admin Dashboard - {admin.getName()}")
    win.geometry("300x200")

    tk.Label(win, text=f"Welcome Admin {admin.getName()}!").pack(pady=10)
    tk.Button(win, text="Logout", command=win.destroy).pack(pady=10)

    win.mainloop()
