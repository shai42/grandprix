import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import pickle
import re

# -------------------- THE CLASS IMPLEMENTATIONS ----------------#
class User:
    def __init__(self, userID, name, email, password):
        self.userID = userID
        self.name = name
        self.email = email
        self.password = password
        self.purchase_history = PurchaseHistory()

    def login(self, email, password):
        return self.email == email and self.password == password

    def view_history(self):
        return self.purchase_history.get_history()

class Admin(User):
    def view_sales_data(self):
        try:
            with open('tickets.pkl', 'rb') as f:
                tickets = pickle.load(f)
            return len(tickets)
        except FileNotFoundError:
            return 0
        
    def manage_discounts(self):
        DiscountManager().manage_discounts()

class Ticket:
    def __init__(self, ticketID, price):
        self.ticketID = ticketID
        self.price = price
        self.issueDate = datetime.now()
        self.seat = None

    def calculate_price(self):
        return self.price

class SingleRacePass(Ticket):
    def calculate_price(self):
        return self.price * 0.95  # 5% discount

class WeekendPackage(Ticket):
    def calculate_price(self):
        return self.price * 0.85  # 15% discount

class SeasonMembership(Ticket):
    def calculate_price(self):
        return self.price * 0.75  # 25% discount

class GroupDiscount(Ticket):
    def calculate_price(self, quantity):
        if quantity >= 5:
            return self.price * 0.80  # 20% discount
        return self.price

class Venue:
    def __init__(self, venueID, location, capacity, rows, seats_per_row):
        self.venueID = venueID
        self.location = location
        self.capacity = capacity
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats = [[Seat(f"{r}-{s}") for s in range(1, seats_per_row+1)] 
                      for r in range(1, rows+1)]

    def get_available_seats(self):
        return [seat for row in self.seats for seat in row if not seat.is_reserved]

class Seat:
    def __init__(self, seatID):
        self.seatID = seatID
        self.is_reserved = False

    def reserve(self):
        if not self.is_reserved:
            self.is_reserved = True
            return True
        return False

class Discount:
    def __init__(self, discountID, description, percentage):
        self.discountID = discountID
        self.description = description
        self.percentage = percentage

    def get_discountID(self):
        return self.discountID
    
    def set_discountID(self, discountID):
        self.discountID = discountID
    
    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description
    
    def get_percentage(self):
        return self.percentage
    
    def set_percentage(self, percentage):
        self.percentage = percentage
    
    def apply_discount(self, amount):
        return amount * (1 - self.percentage/100)
    
class DiscountManager:
    def __init__(self):
        try:
            with open('discounts.pkl', 'rb') as f:
                self.discounts = pickle.load(f)
        except FileNotFoundError:
            self.discounts = []

    def save_discounts(self):
        with open('discounts.pkl', 'wb') as f:
            pickle.dump(self.discounts, f)

    def manage_discounts(self):
        management_window = tk.Toplevel()
        management_window.title("Discount Management")
        
        ttk.Label(management_window, text="Discount ID:").grid(row=0, column=0)
        ttk.Label(management_window, text="Description:").grid(row=1, column=0)
        ttk.Label(management_window, text="Percentage:").grid(row=2, column=0)
        
        id_entry = ttk.Entry(management_window)
        desc_entry = ttk.Entry(management_window)
        perc_entry = ttk.Entry(management_window)
        
        id_entry.grid(row=0, column=1)
        desc_entry.grid(row=1, column=1)
        perc_entry.grid(row=2, column=1)
        
        def add_discount():
            try:
                discount = Discount( 
                    int(id_entry.get()),
                    desc_entry.get(),
                    float(perc_entry.get())
                )
                self.discounts.append(discount)
                self.save_discounts()
                messagebox.showinfo("Success", "Discount added successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid discount data: {str(e)}")

        ttk.Button(management_window, text="Add Discount", command=add_discount).grid(row=3, columnspan=2)

class Payment:
    def __init__(self, paymentID, amount, method, card_number=None, expiry=None):
        self.paymentID = paymentID
        self.amount = amount
        self.date = datetime.now()
        self.method = method
        self.card_number = card_number
        self.expiry = expiry

    def process_payment(self):
        if self.validate_card():
            return True
        return False

    def validate_card(self):
        if self.method == "Credit/Debit":
            return re.match(r'^\d{16}$', self.card_number) and re.match(r'^\d{2}/\d{2}$', self.expiry)
        return True

class PurchaseHistory:
    def __init__(self):
        self.tickets = []

    def add_ticket(self, ticket):
        self.tickets.append(ticket)
        
    def get_history(self):
        return self.tickets

# -------------------- GUI IMPLEMENTATION --------------------
class GrandPrixApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Grand Prix Experience")
        self.style = ttk.Style()
        self.style.configure('TButton', padding=6, relief="flat", background="#4CAF50")
        
        # Create custom styles for seat buttons
        self.style.configure('green.TButton', background='green')
        self.style.configure('red.TButton', background='red')
        
        self.current_user = None
        self.venue = Venue(1, "Silverstone Circuit", 150000, 50, 300)
        self.load_data()
        self.create_login_frame()

    def load_data(self):
        try:
            with open('users.pkl', 'rb') as f:
                self.users = pickle.load(f)
            with open('discounts.pkl', 'rb') as f:
                self.discounts = pickle.load(f)
        except FileNotFoundError:
            self.users = []
            self.discounts = []

    def save_data(self):
        with open('users.pkl', 'wb') as f:
            pickle.dump(self.users, f)
        with open('discounts.pkl', 'wb') as f:
            pickle.dump(self.discounts, f)

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.login_frame.pack()
        
        ttk.Label(self.login_frame, text="Grand Prix Experience", font=('Arial', 16)).grid(row=0, columnspan=2, pady=10)
        
        ttk.Label(self.login_frame, text="Email:").grid(row=1, column=0)
        self.email_entry = ttk.Entry(self.login_frame)
        self.email_entry.grid(row=1, column=1)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1)
        
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=3, column=0, pady=10)
        ttk.Button(self.login_frame, text="Register", command=self.create_registration_frame).grid(row=3, column=1, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        for user in self.users:
            if user.login(email, password):
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome, {user.name}!")
                self.show_dashboard()
                return
        
        messagebox.showerror("Error", "Invalid email or password")

    def create_registration_frame(self):
        reg_window = tk.Toplevel()
        reg_window.title("Registration")
        
        ttk.Label(reg_window, text="Name:").grid(row=0, column=0)
        name_entry = ttk.Entry(reg_window)
        name_entry.grid(row=0, column=1)
        
        ttk.Label(reg_window, text="Email:").grid(row=1, column=0)
        email_entry = ttk.Entry(reg_window)
        email_entry.grid(row=1, column=1)
        
        ttk.Label(reg_window, text="Password:").grid(row=2, column=0)
        password_entry = ttk.Entry(reg_window, show="*")
        password_entry.grid(row=2, column=1)
        
        ttk.Label(reg_window, text="Admin Code (if applicable):").grid(row=3, column=0)
        admin_code_entry = ttk.Entry(reg_window, show="*")
        admin_code_entry.grid(row=3, column=1)
        
        def register_user():
            try:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email_entry.get()):
                    raise ValueError("Invalid email format")
                
                if any(user.email == email_entry.get() for user in self.users):
                    raise ValueError("Email already registered")
                
                new_id = len(self.users) + 1
                if admin_code_entry.get() == "ADMIN123":
                    new_user = Admin(new_id, name_entry.get(), email_entry.get(), password_entry.get())
                else:
                    new_user = User(new_id, name_entry.get(), email_entry.get(), password_entry.get())
                
                self.users.append(new_user)
                self.save_data()
                messagebox.showinfo("Success", "Registration successful!")
                reg_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(reg_window, text="Register", command=register_user).grid(row=4, columnspan=2)

    def clear_frames(self):
        # Clear all frames from the root window
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_frames()
        
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text=f"Welcome, {self.current_user.name}!", font=('Arial', 16)).pack(pady=10)
        
        ticket_frame = ttk.LabelFrame(main_frame, text="Ticket Options", padding=10)
        ticket_frame.pack(fill="both", expand=True, pady=10)
        
        ttk.Button(ticket_frame, text="Single Race Pass", 
                  command=lambda: self.show_seat_selection(SingleRacePass)).pack(fill="x", pady=5)
        
        ttk.Button(ticket_frame, text="Weekend Package", 
                  command=lambda: self.show_seat_selection(WeekendPackage)).pack(fill="x", pady=5)
        
        ttk.Button(ticket_frame, text="Season Membership", 
                  command=lambda: self.show_seat_selection(SeasonMembership)).pack(fill="x", pady=5)
        
        history_button = ttk.Button(main_frame, text="View Purchase History", 
                                   command=self.show_purchase_history)
        history_button.pack(pady=5)
        
        logout_button = ttk.Button(main_frame, text="Logout", command=self.logout)
        logout_button.pack(pady=5)
        
        # Show admin dashboard if user is an admin
        if isinstance(self.current_user, Admin):
            self.show_admin_dashboard()

    def show_purchase_history(self):
        history_window = tk.Toplevel()
        history_window.title("Purchase History")
        
        tickets = self.current_user.view_history()
        
        if not tickets:
            ttk.Label(history_window, text="No purchase history found.").pack(padx=20, pady=20)
        else:
            for i, ticket in enumerate(tickets):
                ticket_frame = ttk.LabelFrame(history_window, text=f"Ticket #{ticket.ticketID}")
                ticket_frame.pack(fill="x", padx=10, pady=5)
                
                ttk.Label(ticket_frame, text=f"Issue Date: {ticket.issueDate.strftime('%Y-%m-%d')}").pack(anchor="w")
                ttk.Label(ticket_frame, text=f"Price: ${ticket.calculate_price():.2f}").pack(anchor="w")
                
                if ticket.seat:
                    ttk.Label(ticket_frame, text=f"Seat: {ticket.seat.seatID}").pack(anchor="w")

    def show_seat_selection(self, ticket_type):
        seat_window = tk.Toplevel()
        seat_window.title("Select Your Seat")
        
        canvas = tk.Canvas(seat_window)
        scrollbar = ttk.Scrollbar(seat_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create a smaller subset of seats for demonstration purposes
        row_limit = min(10, self.venue.rows)
        col_limit = min(10, self.venue.seats_per_row)
        
        for r in range(row_limit):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack()
            for s in range(col_limit):
                seat = self.venue.seats[r][s]
                bg = "green" if not seat.is_reserved else "red"
                btn = ttk.Button(row_frame, text=seat.seatID, width=4,
                               state="disabled" if seat.is_reserved else "normal",
                               style=f"{bg}.TButton")
                btn.grid(row=r, column=s, padx=2, pady=2)
                btn.configure(command=lambda s=seat: self.finalize_purchase(s, ticket_type))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def finalize_purchase(self, seat, ticket_type):
        if seat.reserve():
            ticket = ticket_type(len(self.current_user.purchase_history.tickets) + 1, 100)
            ticket.seat = seat
            payment_window = tk.Toplevel()
            payment_window.title("Payment Details")
            
            ttk.Label(payment_window, text="Payment Method:").grid(row=0, column=0)
            method_var = tk.StringVar()
            ttk.Combobox(payment_window, textvariable=method_var, 
                        values=["Credit/Debit", "Digital Wallet"]).grid(row=0, column=1)
            
            ttk.Label(payment_window, text="Card Number:").grid(row=1, column=0)
            card_entry = ttk.Entry(payment_window)
            card_entry.grid(row=1, column=1)
            
            ttk.Label(payment_window, text="Expiry (MM/YY):").grid(row=2, column=0)
            expiry_entry = ttk.Entry(payment_window)
            expiry_entry.grid(row=2, column=1)
            
            def process_payment():
                payment = Payment(
                    len(self.current_user.purchase_history.tickets) + 1,
                    ticket.calculate_price(),
                    method_var.get(),
                    card_entry.get(),
                    expiry_entry.get()
                )
                if payment.process_payment():
                    self.current_user.purchase_history.add_ticket(ticket)
                    self.save_data()
                    messagebox.showinfo("Success", "Ticket purchased successfully!")
                    payment_window.destroy()
                else:
                    messagebox.showerror("Error", "Payment failed. Please check your details.")
            
            ttk.Button(payment_window, text="Complete Purchase", command=process_payment).grid(row=3, columnspan=2)

    def show_admin_dashboard(self):
        admin_frame = ttk.LabelFrame(self.root, text="Admin Dashboard", padding=10)
        admin_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        sales = self.current_user.view_sales_data()
        ttk.Label(admin_frame, text=f"Total Tickets Sold: {sales}").pack(pady=5)
        
        ttk.Button(admin_frame, text="Manage Discounts", 
                  command=self.current_user.manage_discounts).pack(fill="x", pady=5)
        
        ttk.Button(admin_frame, text="View Venue Status",
                  command=lambda: messagebox.showinfo("Venue Status", 
                  f"Available Seats: {len(self.venue.get_available_seats())}")).pack(fill="x", pady=5)

    def logout(self):
        self.current_user = None
        self.clear_frames()
        self.create_login_frame()

if __name__ == "__main__":
    app = GrandPrixApp()
    app.root.mainloop()
