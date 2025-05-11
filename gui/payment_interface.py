import tkinter as tk
from tkinter import messagebox
import pickle
import os

PAYMENT_FILE = 'data/payments.pkl'

def save_payment(payment_data):
    if not os.path.exists(PAYMENT_FILE):
        with open(PAYMENT_FILE, 'wb') as f:
            pickle.dump([], f)
    with open(PAYMENT_FILE, 'rb') as f:
        payments = pickle.load(f)
    payments.append(payment_data)
    with open(PAYMENT_FILE, 'wb') as f:
        pickle.dump(payments, f)

def open_payment_window(order, user):
    window = tk.Toplevel()
    window.title("Payment Interface")
    window.geometry("300x300")

    tk.Label(window, text="Select Payment Method").pack(pady=5)
    method_var = tk.StringVar()
    method_var.set("Credit Card")
    tk.OptionMenu(window, method_var, "Credit Card", "Digital Wallet", "Debit Card").pack()

    tk.Label(window, text="Card/Wallet Name:").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    def confirm_payment():
        method = method_var.get()
        name = name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        payment_info = {
            "user_email": user.getEmail(),
            "order_id": order['ticket_id'],
            "method": method,
            "name": name,
            "amount": order['price']
        }
        save_payment(payment_info)
        messagebox.showinfo("Success", "Payment Confirmed! Your order is complete.")
        window.destroy()

    tk.Button(window, text="Confirm Payment", command=confirm_payment).pack(pady=10)
