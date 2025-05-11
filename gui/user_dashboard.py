import tkinter as tk

def open_user_dashboard(user):
    win = tk.Tk()
    win.title(f"User Dashboard - {user.getName()}")
    win.geometry("300x200")

    tk.Label(win, text=f"Welcome {user.getName()}!").pack(pady=10)
    tk.Button(win, text="Logout", command=win.destroy).pack(pady=10)

    win.mainloop()
