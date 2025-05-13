import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import pickle
import re
import os
# -------------------- CUSTOM EXCEPTIONS --------------------#
class InvalidEmailError(Exception):
    pass

class DuplicateUserError(Exception):
    pass

class PaymentError(Exception):
    pass

class InvalidDiscountError(Exception):
    pass
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
        self.event = None  

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

class Event:
    def __init__(self, eventID, name, date, venue):
        self.eventID = eventID
        self.name = name
        self.date = date  # datetime.date object
        self.venue = venue  # a Venue object

    def get_event_info(self):
        return f"{self.name} at {self.venue.location} on {self.date.strftime('%Y-%m-%d')}"

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
        management_window.geometry("400x300")
        management_window.minsize(400, 300)
        
        content_frame = ttk.Frame(management_window, padding=20)
        content_frame.pack(fill="both", expand=True)
        
        ttk.Label(content_frame, text="Discount ID:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(content_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(content_frame, text="Percentage:").grid(row=2, column=0, sticky="w", pady=5)
        
        id_entry = ttk.Entry(content_frame, width=30)
        desc_entry = ttk.Entry(content_frame, width=30)
        perc_entry = ttk.Entry(content_frame, width=30)
        
        id_entry.grid(row=0, column=1, sticky="ew", padx=5)
        desc_entry.grid(row=1, column=1, sticky="ew", padx=5)
        perc_entry.grid(row=2, column=1, sticky="ew", padx=5)
        
        content_frame.columnconfigure(1, weight=1)
        
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
                management_window.destroy()  # ✅ Close the window after success
            except Exception as e:
                messagebox.showerror("Error", f"Invalid discount data: {str(e)}")

        btn_frame = ttk.Frame(content_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Add Discount", command=add_discount, width=20).pack()

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
from datetime import date
class GrandPrixApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="#f5f0e1")  # Set root window to light beige
        self.root.title("Grand Prix Experience")
        self.root.geometry("1400x900")  # Set initial window size
        self.root.minsize(600, 400)    # Set minimum window size
        
        # Apply a theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # clam allows bg color override

        # Light beige theme styling
        bg_color = "#f5f0e1"
        self.style.configure('.', background=bg_color)
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, font=('Helvetica', 10))
        self.style.configure('Header.TLabel', background=bg_color, font=('Helvetica', 16, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.configure('Large.TButton', font=('Helvetica', 12), padding=8)

        
        # Configure custom colors for seat buttons
        self.style.configure('Available.TButton', background='green')
        self.style.configure('Reserved.TButton', background='red')
        self.style.configure('Selected.TButton', background='blue')  # Added missing style
        
        self.current_user = None
        self.venue = Venue(1, "Silverstone Circuit", 150000, 10, 10)
        self.events = [
            Event(1, "Silverstone GP", date(2025, 6, 1), self.venue),
            Event(2, "Monaco GP", date(2025, 6, 15), self.venue),
            Event(3, "Yas Marina GP", date(2025, 7, 1), self.venue)
        ]       
        self.load_data()
        
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Create login frame
        self.create_login_frame()

    def load_data(self):
        try:
            with open('users.pkl', 'rb') as f:
                self.users = pickle.load(f)
                print(f"✅ Loaded {len(self.users)} users from file.")
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("⚠️ No users file found or it was empty/corrupted.")
            self.users = []

        try:
            with open('discounts.pkl', 'rb') as f:
                self.discounts = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.discounts = []

    def strip_gui_from_users(self):
        for user in self.users:
            for ticket in user.purchase_history.get_history():
                if ticket.seat and hasattr(ticket.seat, "button"):
                    del ticket.seat.button
    def strip_gui_from_venue(self):
        for row in self.venue.seats:
            for seat in row:
                if hasattr(seat, "button"):
                    del seat.button

    def save_data(self):
        self.strip_gui_from_users()
        self.strip_gui_from_venue()
        with open('users.pkl', 'wb') as f:
            pickle.dump(self.users, f)
        print(f"💾 Saving {len(self.users)} users...")
        with open('discounts.pkl', 'wb') as f:
            pickle.dump(self.discounts, f)


    def create_login_frame(self):
        self.clear_main_container()
        
        # Center the login form
        spacer_top = ttk.Frame(self.main_container)
        spacer_top.pack(fill="both", expand=True)
        
        self.login_frame = ttk.Frame(self.main_container, padding=20, relief="ridge", borderwidth=2)
        self.login_frame.pack(fill="both", padx=50, pady=20)
        
        # Make login form elements expand with window
        self.login_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.login_frame, text="Grand Prix Experience", style='Header.TLabel').grid(row=0, columnspan=2, pady=10)
        
        ttk.Label(self.login_frame, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(self.login_frame)
        self.email_entry.grid(row=1, column=1, sticky="ew", padx=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, sticky="ew", padx=5)
        
        button_frame = ttk.Frame(self.login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Login", command=self.login, width=12).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Register", command=self.create_registration_frame, width=12).pack(side="left", padx=5)
        
        spacer_bottom = ttk.Frame(self.main_container)
        spacer_bottom.pack(fill="both", expand=True)

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
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Registration")
        reg_window.geometry("500x350")
        reg_window.minsize(400, 300)
        
        content_frame = ttk.Frame(reg_window, padding=20)
        content_frame.pack(fill="both", expand=True)
        
        # Make form elements responsive
        content_frame.columnconfigure(1, weight=1)
        
        ttk.Label(content_frame, text="Registration", style='Header.TLabel').grid(row=0, columnspan=2, pady=10)
        
        ttk.Label(content_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(content_frame)
        name_entry.grid(row=1, column=1, sticky="ew", padx=5)
        
        ttk.Label(content_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        email_entry = ttk.Entry(content_frame)
        email_entry.grid(row=2, column=1, sticky="ew", padx=5)
        
        ttk.Label(content_frame, text="Password:").grid(row=3, column=0, sticky="w", pady=5)
        password_entry = ttk.Entry(content_frame, show="*")
        password_entry.grid(row=3, column=1, sticky="ew", padx=5)
        
        ttk.Label(content_frame, text="Admin Code (if applicable):").grid(row=4, column=0, sticky="w", pady=5)
        admin_code_entry = ttk.Entry(content_frame, show="*")
        admin_code_entry.grid(row=4, column=1, sticky="ew", padx=5)
        
        def register_user():
            try:
                email= email_entry.get()
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    raise InvalidEmailError("Invalid email format")
                
                if any(user.email == email_entry.get() for user in self.users):
                    raise DuplicateUserError("Email already registered.")
                
                new_id = len(self.users) + 1
                if admin_code_entry.get() == "ADMIN123":
                    new_user = Admin(new_id, name_entry.get(), email_entry.get(), password_entry.get())
                else:
                    new_user = User(new_id, name_entry.get(), email_entry.get(), password_entry.get())
                
                self.users.append(new_user)
                print(f"✅ Registered user: {new_user.email}")
                self.save_data()
                messagebox.showinfo("Success", "Registration successful!")
                reg_window.destroy()
            except (InvalidEmailError, DuplicateUserError) as e:
                messagebox.showerror("Error", str(e))
        
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Register", command=register_user, width=15).pack()

    def clear_main_container(self):
        # Clear all widgets from the main container
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_container()
        
        # Create a responsive dashboard layout
        dashboard_frame = ttk.Frame(self.main_container, padding=20)
        dashboard_frame.pack(fill="both", expand=True)
        
        # Configure column weights for responsiveness
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=10)
        
        ttk.Label(header_frame, text=f"Welcome, {self.current_user.name}!", style='Header.TLabel').pack(side="left")
        ttk.Button(header_frame, text="Logout", command=self.logout, width=10).pack(side="right")
        
        # Main content with tickets and management options
        content_frame = ttk.Frame(dashboard_frame)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel with ticket options
        left_panel = ttk.LabelFrame(content_frame, text="Ticket Options", padding=10)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        ticket_buttons_frame = ttk.Frame(left_panel)
        ticket_buttons_frame.pack(fill="both", expand=True)
        
        ticket_options = [
            (SingleRacePass, "Single Race Pass", "$100 – One race access. Basic seating."),
            (WeekendPackage, "Weekend Package", "$180 – Whole weekend. Premium zone access."),
            (SeasonMembership, "Season Membership", "$500 – All races. VIP lounges, priority seating."),
            (GroupDiscount, "Group Discount", "$80 per ticket – Min 5 tickets. Group seating.")
        ]

        for ticket_type, label, desc in ticket_options:
            ttk.Label(ticket_buttons_frame, text=desc).pack(pady=(5, 0))
            btn = ttk.Button(ticket_buttons_frame, text=label, style="Large.TButton",
                            command=lambda t=ticket_type: self.select_event_before_booking(t))
            btn.pack(fill="x", padx=5, pady=(0, 10))
        
        # Bottom buttons
        bottom_frame = ttk.Frame(dashboard_frame)
        bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
        ttk.Button(bottom_frame, text="My Profile", 
           command=self.show_user_profile, width=20).pack(pady=5)

        ttk.Button(bottom_frame, text="View Purchase History", 
                 command=self.show_purchase_history, width=20).pack(pady=5)
        
        ttk.Button(bottom_frame, text="View Race Info", command=self.show_race_info, width=20).pack(pady=5)

        # Show admin dashboard if user is an admin
        if isinstance(self.current_user, Admin):
            self.show_admin_dashboard(dashboard_frame)
            
    def show_user_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("My Profile")
        profile_window.geometry("400x300")
    
        main_frame = ttk.Frame(profile_window, padding=20)
        main_frame.pack(fill="both", expand=True)
    
        ttk.Label(main_frame, text="Edit Profile", style="Header.TLabel").grid(row=0, columnspan=2, pady=10)

        ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(main_frame)
        name_entry.insert(0, self.current_user.name)
        name_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        email_entry = ttk.Entry(main_frame)
        email_entry.insert(0, self.current_user.email)
        email_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky="w", pady=5)
        password_entry = ttk.Entry(main_frame, show="*")
        password_entry.insert(0, self.current_user.password)
        password_entry.grid(row=3, column=1, sticky="ew")

        def save_profile():
            try:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email_entry.get()):
                    raise InvalidEmailError("Invalid email format.")
                self.current_user.name = name_entry.get()
                self.current_user.email = email_entry.get()
                self.current_user.password = password_entry.get()
                self.save_data()
                messagebox.showinfo("Success", "Profile updated.")
                profile_window.destroy()
            except InvalidEmailError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(main_frame, text="Save Changes", command=save_profile).grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(main_frame, text="Delete My Account", command=lambda: self.delete_current_account(profile_window), style="TButton").grid(row=5, column=0, columnspan=2, pady=10)
        
    def delete_current_account(self, window):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete your account? This action is irreversible."):
            self.users = [u for u in self.users if u.userID != self.current_user.userID]
            self.save_data()
            messagebox.showinfo("Deleted", "Your account has been deleted.")
            window.destroy()
            self.current_user = None
            self.create_login_frame()


    def show_purchase_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Purchase History")
    
        # Set dynamic window size based on number of tickets
        tickets = self.current_user.view_history()
        height = 200 + len(tickets) * 120 if tickets else 300
        width = 600
        history_window.geometry(f"{width}x{height}")

        main_frame = ttk.Frame(history_window, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Purchase History", style='Header.TLabel').pack(anchor="w", pady=(0, 10))

        if not tickets:
            ttk.Label(main_frame, text="No purchase history found.").pack(padx=20, pady=20)
        else:
            for ticket in tickets:
                ticket_frame = ttk.LabelFrame(main_frame, text=f"Ticket #{ticket.ticketID}", padding=10)
                ticket_frame.pack(fill="x", pady=5)

                ttk.Label(ticket_frame, text=f"Issue Date: {ticket.issueDate.strftime('%Y-%m-%d')}").pack(anchor="w")
                ttk.Label(ticket_frame, text=f"Price: ${ticket.calculate_price():.2f}").pack(anchor="w")
                if ticket.seat:
                    ttk.Label(ticket_frame, text=f"Seat: {ticket.seat.seatID}").pack(anchor="w")
                if ticket.event:
                    ttk.Label(ticket_frame, text=f"Event: {ticket.event.get_event_info()}").pack(anchor="w")

                def delete_ticket(t=ticket):
                    if messagebox.askyesno("Confirm", "Are you sure you want to delete this ticket?"):
                        t.seat.is_reserved = False
                        self.current_user.purchase_history.tickets.remove(t)
                        self.save_data()
                        messagebox.showinfo("Deleted", "Ticket removed successfully.")
                        history_window.destroy()
                        self.show_purchase_history()

                ttk.Button(ticket_frame, text="Cancel Ticket", command=delete_ticket).pack(anchor="e", pady=5)

    def select_event_before_booking(self, ticket_type):
        event_window = tk.Toplevel(self.root)
        event_window.title("Select Event")
        event_window.geometry("400x200")

        frame = ttk.Frame(event_window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Choose an Event:", style='Header.TLabel').pack(pady=10)

        event_var = tk.StringVar()
        events = [
            ("2025-06-01", "Silverstone"),
            ("2025-06-15", "Monaco"),
            ("2025-07-01", "Yas Marina")
        ]
        combo = ttk.Combobox(frame, textvariable=event_var, state="readonly",
                         values=[f"{date} – {name}" for date, name in events])
        combo.pack(pady=10)
        combo.current(0)

        def proceed():
            selected = combo.get().split(" – ")[0]
            event_window.destroy()
            self.show_seat_selection(ticket_type, selected)

        ttk.Button(frame, text="Continue", command=proceed).pack(pady=10)
    
    def show_race_info(self):
        info_window = tk.Toplevel(self.root)
        info_window.title("Race & Venue Info")
        info_window.geometry("500x400")

        frame = ttk.Frame(info_window, padding=20)
        frame.pack(fill="both", expand=True)

        info = (
            "Upcoming Races:\n"
            "- 1st June 2025 - Silverstone\n"
            "- 15th June 2025 - Monaco\n"
            "- 1st July 2025 - Yas Marina\n\n"
            "Venue Services:\n"
            "- Free Parking\n"
            "- Food Courts\n"
            "- VIP Lounges\n"
            "- Shuttle Buses"
        )

        ttk.Label(frame, text=info, justify="left", style='TLabel').pack(anchor="w")
    
    def show_seat_selection(self, ticket_type, preselected_date=None):
        seat_window = tk.Toplevel(self.root)
        seat_window.title("Select Your Seat")

        # Calculate window size dynamically
        seat_width = 50
        seat_height = 40
        padding = 150
        total_width = self.venue.seats_per_row * seat_width + padding
        total_height = self.venue.rows * seat_height + 250
        seat_window.geometry(f"{total_width}x{total_height}")

        main_frame = ttk.Frame(seat_window, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Select Your Seat", style='Header.TLabel').pack(pady=(0, 15))

        group_var = tk.BooleanVar()
        group_check = ttk.Checkbutton(main_frame, text="Group Purchase (5+ tickets)", variable=group_var)
        group_check.pack(pady=5)

        selected_seats = []

        seat_frame = ttk.Frame(main_frame)
        seat_frame.pack()

        for r in range(self.venue.rows):
            for s in range(self.venue.seats_per_row):
                seat = self.venue.seats[r][s]
                style = "Reserved.TButton" if seat.is_reserved else "Available.TButton"
                state = "disabled" if seat.is_reserved else "normal"

                btn = ttk.Button(seat_frame, text=seat.seatID, width=4, state=state, style=style)
                btn.grid(row=r, column=s, padx=2, pady=2)

                if not seat.is_reserved:
                    seat.button = btn

                    def toggle_seat(s=seat, b=btn):
                        if s in selected_seats:
                            selected_seats.remove(s)
                            b.configure(style="Available.TButton")
                        else:
                            selected_seats.append(s)
                            b.configure(style="Selected.TButton")

                    btn.configure(command=toggle_seat)

        legend_frame = ttk.Frame(main_frame)
        legend_frame.pack(pady=15)

        ttk.Label(legend_frame, text="Available", background="green", width=10).pack(side="left", padx=10)
        ttk.Label(legend_frame, text="Selected", background="blue", width=10).pack(side="left", padx=10)
        ttk.Label(legend_frame, text="Reserved", background="red", width=10).pack(side="left", padx=10)

        def proceed_to_payment():
            event = next((e for e in self.events if str(e.date) == preselected_date), None)
            if not event:
                messagebox.showerror("Error", "Selected event not found.")
                return

            if not selected_seats:
                messagebox.showwarning("No Selection", "Please select at least one seat.")
                return

            self.finalize_purchase(selected_seats, ticket_type, group_var.get(), event)
            seat_window.destroy()

        ttk.Button(main_frame, text="Continue to Payment", command=proceed_to_payment, style="Large.TButton").pack(pady=10)
    
    def get_next_ticket_id(self):
        try:
            with open('tickets.pkl', 'rb') as f:
                tickets = pickle.load(f)
                if tickets:  # If there are tickets, get the highest ID
                    return max(t.ticketID for t in tickets) + 1
                return 1
        except (FileNotFoundError, EOFError):
            return 1
        
    def finalize_purchase(self, seats, ticket_type, is_group=False, event=None):
        selected_seats = []  # To track all selected seats
        total_price = 0      # To track the total price for all tickets

        # Group purchase logic (applies to all seats as a single group)
        if is_group:
            quantity = simpledialog.askinteger("Group Purchase", 
                                        "How many tickets in your group?",
                                        minvalue=5, maxvalue=20)
            if quantity is None:  # User cancelled
                return
        else:
            quantity = len(seats)  # Each seat counts as one

        # Loop over each seat in the selection
        for seat in seats:
            
            if len(self.venue.get_available_seats()) < len(seats):
                messagebox.showerror("Full", "Not enough seats available for your group.")
                return

            if seat.reserve():
                ticket_id = self.get_next_ticket_id()
            
                # Calculate price for this seat
                ticket = GroupDiscount(ticket_id, 100) if is_group else ticket_type(ticket_id, 100)
            
                # For group discount, the price is calculated once for each seat
                if is_group:
                    price = ticket.calculate_price(quantity) 
                else:
                    price = ticket.calculate_price()
                
                total_price += price  # Add to the total price
            
                ticket.seat = seat
                ticket.event = event
                selected_seats.append(ticket)  # Track this ticket for later payment
            else:
                messagebox.showwarning("Seat Not Available", f"Seat {seat.seatID} is already reserved.")
                # Undo all reservations made so far
                for s in selected_seats:
                    s.seat.is_reserved = False
                return  # Exit if a seat is unavailable
        
        # Payment window and payment details
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Payment Details")
        payment_window.geometry("500x300")
        payment_window.minsize(400, 250)

        main_frame = ttk.Frame(payment_window, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Configure grid for responsiveness
        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Payment Details", style='Header.TLabel').grid(
        row=0, column=0, columnspan=2, pady=(0, 15))

        # Payment Method selection
        tk.Label(main_frame, text="Payment Method:").grid(row=1, column=0, sticky="w", pady=5)
        method_var = tk.StringVar()
        method_combo = ttk.Combobox(main_frame, textvariable=method_var, 
                                    values=["Credit/Debit", "Digital Wallet"])
        method_combo.grid(row=1, column=1, sticky="ew", padx=5)
        method_combo.current(0)

        # Card Number and Expiry inputs
        card_label = ttk.Label(main_frame, text="Card Number:")
        card_label.grid(row=2, column=0, sticky="w", pady=5)
        card_entry = ttk.Entry(main_frame)
        card_entry.grid(row=2, column=1, sticky="ew", padx=5)

        expiry_label = ttk.Label(main_frame, text="Expiry (MM/YY):")
        expiry_label.grid(row=3, column=0, sticky="w", pady=5)
        expiry_entry = ttk.Entry(main_frame)
        expiry_entry.grid(row=3, column=1, sticky="ew", padx=5)

        # Function to hide/show card fields based on method
        def update_payment_fields(*args):
            if method_var.get() == "Credit/Debit":
                card_label.grid()
                card_entry.grid()
                expiry_label.grid()
                expiry_entry.grid()
            else:
                card_entry.delete(0, 'end')
                expiry_entry.delete(0, 'end')
                card_label.grid_remove()
                card_entry.grid_remove()
                expiry_label.grid_remove()
                expiry_entry.grid_remove()

        method_var.trace_add("write", update_payment_fields)
        update_payment_fields()


        # Price information
        price_frame = ttk.Frame(main_frame)
        price_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(price_frame, text=f"Total Price: ${total_price:.2f}",  # Use total_price here
            font=('Helvetica', 12, 'bold')).pack(side="right")

        # Create the button frame here
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        def process_payment():
            payment = Payment(
                len(self.current_user.purchase_history.tickets) + 1,
                total_price,
                method_var.get(),
                card_entry.get(),
                expiry_entry.get()
            )

            if not payment.process_payment():
                messagebox.showerror("Error", "Payment failed. Please check your details.")
                # Unreserve the seats
                for ticket in selected_seats:
                    ticket.seat.is_reserved = False
                return

            # If payment is successful, add all tickets to purchase history
            for ticket in selected_seats:
                if hasattr(ticket.seat, "button"):
                    del ticket.seat.button  # Remove GUI reference before pickling
                self.current_user.purchase_history.add_ticket(ticket)
                try:
                    self.save_ticket(ticket)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save ticket: {e}")
                    return

            self.save_data()  # ✅ This now runs only after successful payment and data prep
            messagebox.showinfo("Success", "Tickets purchased successfully!")
            payment_window.destroy()

        ttk.Button(button_frame, text="Complete Purchase", command=process_payment, 
                    style="Large.TButton", width=20).pack()



    def save_ticket(self, ticket):
        import traceback

        # Try to load existing tickets or create empty list
        try:
            with open('tickets.pkl', 'rb') as f:
                all_tickets = pickle.load(f)
        except (FileNotFoundError, EOFError):
            all_tickets = []

        # Remove GUI reference before saving
        if ticket.seat and hasattr(ticket.seat, "button"):
            print("🔍 Removing seat.button from ticket before saving")
            del ticket.seat.button

        all_tickets.append(ticket)
        self.strip_gui_from_venue()

        try:
            print("💾 Attempting to save ticket...")
            with open('tickets.pkl', 'wb') as f:
                pickle.dump(all_tickets, f)
            print("✅ Ticket saved successfully.")
        except Exception as e:
            print("❌ Exception during ticket saving:")
            traceback.print_exc()  # Prints full error in console
            messagebox.showerror("Error", f"Failed to save ticket: {e}")
            raise

    def show_admin_dashboard(self, parent_frame):
        admin_frame = ttk.LabelFrame(parent_frame, text="Admin Dashboard", padding=10)
        admin_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        # Create a two-column layout for admin controls
        admin_content = ttk.Frame(admin_frame)
        admin_content.pack(fill="both", expand=True)
        admin_content.columnconfigure(0, weight=1)
        admin_content.columnconfigure(1, weight=1)
        
        # Sales data
        sales = self.current_user.view_sales_data()
        sales_frame = ttk.Frame(admin_content)
        sales_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ttk.Label(sales_frame, text="Sales Data", font=('Helvetica', 12, 'bold')).pack(anchor="w")
        ttk.Label(sales_frame, text=f"Total Tickets Sold: {sales}").pack(anchor="w", pady=5)
        
        # Admin controls
        controls_frame = ttk.Frame(admin_content)
        controls_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Manage Discounts", 
                 command=self.current_user.manage_discounts, width=20).pack(fill="x", pady=5)
        
        ttk.Button(controls_frame, text="View Venue Status",
                 command=lambda: messagebox.showinfo("Venue Status", 
                 f"Available Seats: {len(self.venue.get_available_seats())}"), 
                 width=20).pack(fill="x", pady=5)

    def logout(self):
        """Log out the current user and return to the login screen."""
        self.current_user = None
        self.create_login_frame()

if __name__ == "__main__":
    # Create necessary files if they don't exist
    if not os.path.exists('users.pkl'):
        with open('users.pkl', 'wb') as f:
            pickle.dump([], f)
    
    if not os.path.exists('tickets.pkl'):
        with open('tickets.pkl', 'wb') as f:
            pickle.dump([], f)
    
    if not os.path.exists('discounts.pkl'):
        with open('discounts.pkl', 'wb') as f:
            pickle.dump([], f)

    app = GrandPrixApp()
    app.root.mainloop()
