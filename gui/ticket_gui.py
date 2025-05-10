"""
Ticket management GUI for the Grand Prix Experience ticket booking system.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data.manager import DataManager
from models.ticket import SingleRacePass, WeekendPackage, SeasonMembership, GroupDiscount
from models.discount import Discount

class TicketsGUI:
    def __init__(self, root, user=None):
        """
        Initialize the tickets GUI.
        
        Args:
            root: The tkinter root window
            user: The currently logged-in user
        """
        self.root = root
        self.user = user
        self.data_manager = DataManager()
        
        self.root.title("Grand Prix Experience - Tickets")
        self.root.geometry("800x600")
        
        # Create notebook for different ticket types
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tab for each ticket type
        self.single_race_tab = ttk.Frame(self.notebook)
        self.weekend_tab = ttk.Frame(self.notebook)
        self.season_tab = ttk.Frame(self.notebook)
        self.group_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.single_race_tab, text='Single Race Pass')
        self.notebook.add(self.weekend_tab, text='Weekend Package')
        self.notebook.add(self.season_tab, text='Season Membership')
        self.notebook.add(self.group_tab, text='Group Discount')
        
        # Setup each tab
        self._setup_single_race_tab()
        self._setup_weekend_tab()
        self._setup_season_tab()
        self._setup_group_tab()
    
    def _setup_single_race_tab(self):
        """Setup the Single Race Pass tab."""
        # Load events for selection
        events = self.data_manager.load_events()
        
        # Frame for form
        form_frame = tk.Frame(self.single_race_tab, padx=20, pady=20)
        form_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(form_frame, text="Purchase Single Race Pass", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Event selection
        event_label = tk.Label(form_frame, text="Select Event:")
        event_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.selected_event = tk.StringVar()
        event_names = ["No events available"]
        if events:
            event_names = [f"{event.get_name()} - {event.get_date().strftime('%Y-%m-%d')}" for event in events]
        
        event_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_event, values=event_names, width=40)
        event_dropdown.grid(row=1, column=1, sticky="w", pady=5)
        event_dropdown.current(0)
        
        # Price display
        price_label = tk.Label(form_frame, text="Price:")
        price_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.price_var = tk.StringVar(value="$150.00")
        price_display = tk.Label(form_frame, textvariable=self.price_var, font=("Arial", 12, "bold"))
        price_display.grid(row=2, column=1, sticky="w", pady=5)
        
        # Payment method
        payment_label = tk.Label(form_frame, text="Payment Method:")
        payment_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.payment_method = tk.StringVar()
        payment_methods = ["Credit Card", "Debit Card", "PayPal"]
        payment_dropdown = ttk.Combobox(form_frame, textvariable=self.payment_method, values=payment_methods, width=40)
        payment_dropdown.grid(row=3, column=1, sticky="w", pady=5)
        payment_dropdown.current(0)
        
        # Purchase button
        purchase_button = tk.Button(form_frame, text="Purchase Ticket", command=self.purchase_single_race)
        purchase_button.grid(row=4, column=0, columnspan=2, pady=(20, 0))
    
    def _setup_weekend_tab(self):
        """Setup the Weekend Package tab."""
        # Load events for selection
        events = self.data_manager.load_events()
        
        # Frame for form
        form_frame = tk.Frame(self.weekend_tab, padx=20, pady=20)
        form_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(form_frame, text="Purchase Weekend Package", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Weekend selection (simplified - would need actual weekends in a real app)
        weekend_label = tk.Label(form_frame, text="Select Weekend:")
        weekend_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.selected_weekend = tk.StringVar()
        weekend_options = ["May 17-19, 2025 - Monaco Grand Prix", "June 14-16, 2025 - Canadian Grand Prix"]
        
        weekend_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_weekend, values=weekend_options, width=40)
        weekend_dropdown.grid(row=1, column=1, sticky="w", pady=5)
        weekend_dropdown.current(0)
        
        # Price display
        price_label = tk.Label(form_frame, text="Price:")
        price_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.weekend_price_var = tk.StringVar(value="$350.00")
        price_display = tk.Label(form_frame, textvariable=self.weekend_price_var, font=("Arial", 12, "bold"))
        price_display.grid(row=2, column=1, sticky="w", pady=5)
        
        # Payment method
        payment_label = tk.Label(form_frame, text="Payment Method:")
        payment_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.weekend_payment_method = tk.StringVar()
        payment_methods = ["Credit Card", "Debit Card", "PayPal"]
        payment_dropdown = ttk.Combobox(form_frame, textvariable=self.weekend_payment_method, values=payment_methods, width=40)
        payment_dropdown.grid(row=3, column=1, sticky="w", pady=5)
        payment_dropdown.current(0)
        
        # Purchase button
        purchase_button = tk.Button(form_frame, text="Purchase Weekend Package", command=self.purchase_weekend)
        purchase_button.grid(row=4, column=0, columnspan=2, pady=(20, 0))
    
    def _setup_season_tab(self):
        """Setup the Season Membership tab."""
        # Frame for form
        form_frame = tk.Frame(self.season_tab, padx=20, pady=20)
        form_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(form_frame, text="Purchase Season Membership", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Season selection
        season_label = tk.Label(form_frame, text="Season Year:")
        season_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.selected_season = tk.StringVar(value="2025")
        season_entry = tk.Entry(form_frame, textvariable=self.selected_season, width=10)
        season_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Membership type
        type_label = tk.Label(form_frame, text="Membership Type:")
        type_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.membership_type = tk.StringVar()
        membership_types = ["Standard", "Premium", "VIP"]
        type_dropdown = ttk.Combobox(form_frame, textvariable=self.membership_type, values=membership_types, width=40)
        type_dropdown.grid(row=2, column=1, sticky="w", pady=5)
        type_dropdown.current(0)
        
        # Price display
        price_label = tk.Label(form_frame, text="Price:")
        price_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.season_price_var = tk.StringVar(value="$1,500.00")
        price_display = tk.Label(form_frame, textvariable=self.season_price_var, font=("Arial", 12, "bold"))
        price_display.grid(row=3, column=1, sticky="w", pady=5)
        
        # Payment method
        payment_label = tk.Label(form_frame, text="Payment Method:")
        payment_label.grid(row=4, column=0, sticky="w", pady=5)
        
        self.season_payment_method = tk.StringVar()
        payment_methods = ["Credit Card", "Debit Card", "PayPal"]
        payment_dropdown = ttk.Combobox(form_frame, textvariable=self.season_payment_method, values=payment_methods, width=40)
        payment_dropdown.grid(row=4, column=1, sticky="w", pady=5)
        payment_dropdown.current(0)
        
        # Purchase button
        purchase_button = tk.Button(form_frame, text="Purchase Season Membership", command=self.purchase_season)
        purchase_button.grid(row=5, column=0, columnspan=2, pady=(20, 0))
    
    def _setup_group_tab(self):
        """Setup the Group Discount tab."""
        # Load events for selection
        events = self.data_manager.load_events()
        
        # Frame for form
        form_frame = tk.Frame(self.group_tab, padx=20, pady=20)
        form_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(form_frame, text="Purchase Group Tickets", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Event selection
        event_label = tk.Label(form_frame, text="Select Event:")
        event_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.group_selected_event = tk.StringVar()
        event_names = ["No events available"]
        if events:
            event_names = [f"{event.get_name()} - {event.get_date().strftime('%Y-%m-%d')}" for event in events]
        
        event_dropdown = ttk.Combobox(form_frame, textvariable=self.group_selected_event, values=event_names, width=40)
        event_dropdown.grid(row=1, column=1, sticky="w", pady=5)
        event_dropdown.current(0)
        
        # Group size
        size_label = tk.Label(form_frame, text="Number of People:")
        size_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.group_size = tk.StringVar(value="5")
        size_entry = tk.Entry(form_frame, textvariable=self.group_size, width=10)
        size_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        # Price display
        price_label = tk.Label(form_frame, text="Price (per person):")
        price_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.group_price_var = tk.StringVar(value="$120.00")
        price_display = tk.Label(form_frame, textvariable=self.group_price_var, font=("Arial", 12, "bold"))
        price_display.grid(row=3, column=1, sticky="w", pady=5)
        
        # Total price
        total_label = tk.Label(form_frame, text="Total Price:")
        total_label.grid(row=4, column=0, sticky="w", pady=5)
        
        self.total_price_var = tk.StringVar(value="$600.00")
        total_display = tk.Label(form_frame, textvariable=self.total_price_var, font=("Arial", 12, "bold"))
        total_display.grid(row=4, column=1, sticky="w", pady=5)
        
        # Update price button
        update_button = tk.Button(form_frame, text="Calculate Price", command=self.update_group_price)
        update_button.grid(row=5, column=0, columnspan=2, pady=(10, 10))
        
        # Payment method
        payment_label = tk.Label(form_frame, text="Payment Method:")
        payment_label.grid(row=6, column=0, sticky="w", pady=5)
        
        self.group_payment_method = tk.StringVar()
        payment_methods = ["Credit Card", "Debit Card", "PayPal"]
        payment_dropdown = ttk.Combobox(form_frame, textvariable=self.group_payment_method, values=payment_methods, width=40)
        payment_dropdown.grid(row=6, column=1, sticky="w", pady=5)
        payment_dropdown.current(0)
        
        # Purchase button
        purchase_button = tk.Button(form_frame, text="Purchase Group Tickets", command=self.purchase_group)
        purchase_button.grid(row=7, column=0, columnspan=2, pady=(20, 0))
    
    def update_group_price(self):
        """Update the group price based on group size."""
        try:
            size = int(self.group_size.get())
            price_per_person = 150.0  # Base price
            
            # Apply discount based on group size
            if size >= 10:
                price_per_person *= 0.7  # 30% discount
            elif size >= 5:
                price_per_person *= 0.8  # 20% discount
            else:
                price_per_person *= 0.9  # 10% discount
            
            # Update price labels
            self.group_price_var.set(f"${price_per_person:.2f}")
            total_price = price_per_person * size
            self.total_price_var.set(f"${total_price:.2f}")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for group size.")
    
    def purchase_single_race(self):
        """Handle single race ticket purchase."""
        if not self.user:
            messagebox.showerror("Error", "Please log in to purchase tickets.")
            return
        
        # Get selected event
        event_str = self.selected_event.get()
        
        # In a real app, would find the actual event object
        # For now, just create a ticket
        tickets = self.data_manager.load_tickets()
        
        # Generate a new ticket ID
        ticket_id = 1
        if tickets:
            ticket_id = max(ticket.get_ticket_id() for ticket in tickets) + 1
        
        # Create the ticket
        ticket = SingleRacePass(ticket_id, 150.0, datetime.now(), 1)  # Assuming event_id=1
        tickets.append(ticket)
        
        # Add to user's purchase history
        self.user.get_purchase_history().add_ticket(ticket)
        
        # Save updated tickets and users
        users = self.data_manager.load_users()
        for i, u in enumerate(users):
            if u.get_user_id() == self.user.get_user_id():
                users[i] = self.user
                break
        
        if self.data_manager.save_tickets(tickets) and self.data_manager.save_users(users):
            messagebox.showinfo("Success", f"Single Race Pass purchased for {event_str}!")
        else:
            messagebox.showerror("Error", "Failed to complete purchase. Please try again.")
    
    def purchase_weekend(self):
        """Handle weekend package purchase."""
        if not self.user:
            messagebox.showerror("Error", "Please log in to purchase tickets.")
            return
        
        # Get selected weekend
        weekend_str = self.selected_weekend.get()
        
        # In a real app, would find the actual weekend object
        # For now, just create a ticket
        tickets = self.data_manager.load_tickets()
        
        # Generate a new ticket ID
        ticket_id = 1
        if tickets:
            ticket_id = max(ticket.get_ticket_id() for ticket in tickets) + 1
        
        # Create the ticket
        ticket = WeekendPackage(ticket_id, 350.0, datetime.now(), 1)  # Assuming weekend_id=1
        tickets.append(ticket)
        
        # Add to user's purchase history
        self.user.get_purchase_history().add_ticket(ticket)
        
        # Save updated tickets and users
        users = self.data_manager.load_users()
        for i, u in enumerate(users):
            if u.get_user_id() == self.user.get_user_id():
                users[i] = self.user
                break
        
        if self.data_manager.save_tickets(tickets) and self.data_manager.save_users(users):
            messagebox.showinfo("Success", f"Weekend Package purchased for {weekend_str}!")
        else:
            messagebox.showerror("Error", "Failed to complete purchase. Please try again.")
    
    def purchase_season(self):
        """Handle season membership purchase."""
        if not self.user:
            messagebox.showerror("Error", "Please log in to purchase tickets.")
            return
        
        # Get selected season and membership type
        season_year = self.selected_season.get()
        membership_type = self.membership_type.get()
        
        # In a real app, would validate and process differently based on type
        # For now, just create a ticket
        tickets = self.data_manager.load_tickets()
        
        # Generate a new ticket ID
        ticket_id = 1
        if tickets:
            ticket_id = max(ticket.get_ticket_id() for ticket in tickets) + 1
        
        # Price adjustment based on membership type
        price = 1500.0
        if membership_type == "Premium":
            price = 2500.0
        elif membership_type == "VIP":
            price = 5000.0
        
        # Create the ticket
        ticket = SeasonMembership(ticket_id, price, datetime.now(), int(season_year))
        tickets.append(ticket)
        
        # Add to user's purchase history
        self.user.get_purchase_history().add_ticket(ticket)
        
        # Save updated tickets and users
        users = self.data_manager.load_users()
        for i, u in enumerate(users):
            if u.get_user_id() == self.user.get_user_id():
                users[i] = self.user
                break
        
        if self.data_manager.save_tickets(tickets) and self.data_manager.save_users(users):
            messagebox.showinfo("Success", f"{membership_type} Season Membership purchased for {season_year}!")
        else:
            messagebox.showerror("Error", "Failed to complete purchase. Please try again.")
    
    def purchase_group(self):
        """Handle group ticket purchase."""
        if not self.user:
            messagebox.showerror("Error", "Please log in to purchase tickets.")
            return
        
        try:
            # Get group details
            event_str = self.group_selected_event.get()
            size = int(self.group_size.get())
            
            if size < 2:
                messagebox.showerror("Error", "Group size must be at least 2.")
                return
            
            # In a real app, would find the actual event object
            # For now, just create a ticket
            tickets = self.data_manager.load_tickets()
            
            # Generate a new ticket ID
            ticket_id = 1
            if tickets:
                ticket_id = max(ticket.get_ticket_id() for ticket in tickets) + 1
            
            # Calculate price
            price_per_person = 150.0  # Base price
            
            # Apply discount based on group size
            if size >= 10:
                price_per_person *= 0.7  # 30% discount
            elif size >= 5:
                price_per_person *= 0.8  # 20% discount
            else:
                price_per_person *= 0.9  # 10% discount
            
            total_price = price_per_person * size
            
            # Create the ticket
            ticket = GroupDiscount(ticket_id, total_price, datetime.now(), size)
            tickets.append(ticket)
            
            # Add to user's purchase history
            self.user.get_purchase_history().add_ticket(ticket)
            
            # Save updated tickets and users
            users = self.data_manager.load_users()
            for i, u in enumerate(users):
                if u.get_user_id() == self.user.get_user_id():
                    users[i] = self.user
                    break
            
            if self.data_manager.save_tickets(tickets) and self.data_manager.save_users(users):
                messagebox.showinfo("Success", f"Group tickets purchased for {size} people for {event_str}!")
            else:
                messagebox.showerror("Error", "Failed to complete purchase. Please try again.")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for group size.")