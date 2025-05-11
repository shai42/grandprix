import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from models.ticket import SingleRacePass, WeekendPackage, SeasonMembership, GroupDiscount
from utils.order_utils import save_order
import pickle
import os
import random

def open_ticket_purchase_window(user):
    win = tk.Toplevel()
    win.title("Buy Ticket")
    win.geometry("400x500")

    tk.Label(win, text="Select Ticket Type").pack()
    ticket_var = tk.StringVar(value="SingleRacePass")
    tk.OptionMenu(win, ticket_var, "SingleRacePass", "WeekendPackage", "SeasonMembership", "GroupDiscount").pack()

    tk.Label(win, text="Select Race Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(win)
    date_entry.pack()

    price_label = tk.Label(win, text="Price: AED 0")
    price_label.pack()

    selected_ticket = [None]  # to keep track of the ticket object

    def calculate_price():
        ticket_type = ticket_var.get()
        base_price = 100
        ticket_id = f"T{random.randint(1000,9999)}"
        issue_date = datetime.today().strftime('%Y-%m-%d')

        if ticket_type == "SingleRacePass":
            ticket = SingleRacePass(ticket_id, base_price, issue_date)
        elif ticket_type == "WeekendPackage":
            ticket = WeekendPackage(ticket_id, base_price, issue_date)
        elif ticket_type == "SeasonMembership":
            ticket = SeasonMembership(ticket_id, base_price, issue_date)
        elif ticket_type == "GroupDiscount":
            ticket = GroupDiscount(ticket_id, base_price, issue_date)

        selected_ticket[0] = ticket
        price_label.config(text=f"Price: AED {ticket.calculatePrice():.2f}")

    def confirm_purchase():
        race_date = date_entry.get()
        try:
            datetime.strptime(race_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid race date.")
            return

        ticket = selected_ticket[0]
        if not ticket:
            messagebox.showerror("Missing Info", "Please calculate price first.")
            return

        def open_payment():
            pay_win = tk.Toplevel()
            pay_win.title("Payment")
            pay_win.geometry("300x300")

            tk.Label(pay_win, text="Select Payment Method").pack()
            method_var = tk.StringVar(value="Credit Card")
            tk.OptionMenu(pay_win, method_var, "Credit Card", "Digital Wallet").pack()

            tk.Label(pay_win, text="Card/Wallet Info").pack()
            info_entry = tk.Entry(pay_win)
            info_entry.pack()
            
            def save_payment(payment_data, filename="data/payments.pkl"):
                if os.path.exists(filename):
                   with open(filename, "rb") as file:
                     payments = pickle.load(file)
                else:
                        payments = []

                payments.append(payment_data)

                with open(filename, "wb") as file:
                    pickle.dump(payments, file)
                
            def finalize():
                payment = {
                    "user_email": user.getEmail(),
                    "ticket_id": ticket.getTicketID(),
                    "amount": ticket.calculatePrice(),
                    "method": method_var.get(),
                    "details": info_entry.get(),
                    "payment_date": datetime.today().strftime('%Y-%m-%d')
                }
                save_payment(payment)

                order = {
                    "user_email": user.getEmail(),
                    "ticket_type": ticket.__class__.__name__,
                    "ticket_id": ticket.getTicketID(),
                    "price": ticket.calculatePrice(),
                    "issue_date": ticket.getIssueDate(),
                    "race_date": race_date
                }
                save_order(order)

                messagebox.showinfo("Success", "Purchase & Payment Completed!")
                pay_win.destroy()
                win.destroy()

            tk.Button(pay_win, text="Confirm Payment", command=finalize).pack(pady=10)

        open_payment()

    tk.Button(win, text="Calculate Price", command=calculate_price).pack(pady=5)
    tk.Button(win, text="Proceed to Payment", command=confirm_purchase).pack(pady=10)
