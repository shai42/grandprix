"""
Reservation GUI for the Grand Prix Experience ticket booking system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.reservation import Reservation
from models.ticket import Ticket

class ReservationGUI:
    def __init__(self, master, user):
        self.master = master
        self.user = user        
        self.master.title(f"Grand Prix Experience - Reservations ({self.user.get_name()})")
        self.master.geometry("800x600")
        self.create_widgets()
        self.load_reservations()
    
    def create_widgets(self):
        """Create the reservation management widgets."""
        # Menu Bar
        menubar = tk.Menu(self.master)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Refresh", command=self.load_reservations)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        self.master.config(menu=menubar)
        
        # Main Frame
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Your Reservations", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Reservations Treeview
        self.reservations_tree = ttk.Treeview(main_frame, columns=("ID", "Date", "Status", "Tickets"), show="headings")
        self.reservations_tree.heading("ID", text="Reservation ID")
        self.reservations_tree.heading("Date", text="Date")
        self.reservations_tree.heading("Status", text="Status")
        self.reservations_tree.heading("Tickets", text="Tickets")
        
        self.reservations_tree.column("ID", width=100)
        self.reservations_tree.column("Date", width=150)
        self.reservations_tree.column("Status", width=100)
        self.reservations_tree.column("Tickets", width=200)
        
        self.reservations_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel Reservation", command=self.cancel_reservation).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="New Reservation", command=self.new_reservation).pack(side=tk.RIGHT, padx=5)
    
    def load_reservations(self):
        """Load the user's reservations."""
        # Clear existing items
        for item in self.reservations_tree.get_children():
            self.reservations_tree.delete(item)
        
        reservations = self.data_manager.load_reservations()
        user_reservations = [r for r in reservations if any(t.get_ticket_id() in [t.get_ticket_id() for t in self.user.get_purchase_history().get_history()] for t in r.get_tickets())]
        
        for res in user_reservations:
            self.reservations_tree.insert("", tk.END, values=(
                res.get_reservation_id(),
                res.get_date().strftime("%Y-%m-%d %H:%M"),
                "Confirmed",
                f"{len(res.get_tickets())} tickets"
            ))
    
    def view_details(self):
        """View details of selected reservation."""
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a reservation")
            return
        
        item = self.reservations_tree.item(selected[0])
        res_id = item["values"][0]
        
        reservations = self.data_manager.load_reservations()
        reservation = next((r for r in reservations if r.get_reservation_id() == res_id), None)
        
        if not reservation:
            messagebox.showerror("Error", "Reservation not found")
            return
        
        details_window = tk.Toplevel(self.master)
        details_window.title(f"Reservation Details - #{res_id}")
        details_window.geometry("500x400")
        
        # Details Frame
        details_frame = tk.Frame(details_window)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(details_frame, text=f"Reservation ID: {res_id}", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(details_frame, text=f"Date: {reservation.get_date().strftime('%Y-%m-%d %H:%M')}").pack(anchor="w", pady=5)
        
        # Tickets Frame
        tickets_frame = tk.LabelFrame(details_frame, text="Tickets", padx=10, pady=10)
        tickets_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tickets_tree = ttk.Treeview(tickets_frame, columns=("ID", "Type", "Price"), show="headings")
        tickets_tree.heading("ID", text="Ticket ID")
        tickets_tree.heading("Type", text="Type")
        tickets_tree.heading("Price", text="Price")
        
        tickets_tree.column("ID", width=80)
        tickets_tree.column("Type", width=150)
        tickets_tree.column("Price", width=100)
        
        for ticket in reservation.get_tickets():
            ticket_type = type(ticket).__name__
            tickets_tree.insert("", tk.END, values=(
                ticket.get_ticket_id(),
                ticket_type,
                f"${ticket.get_price():.2f}"
            ))
        
        tickets_tree.pack(fill=tk.BOTH, expand=True)
    
    def cancel_reservation(self):
        """Cancel selected reservation."""
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a reservation")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this reservation?"):
            item = self.reservations_tree.item(selected[0])
            res_id = item["values"][0]
            
            reservations = self.data_manager.load_reservations()
            reservation = next((r for r in reservations if r.get_reservation_id() == res_id), None)
            
            if reservation:
                # In a real app, would also handle ticket availability updates
                reservations.remove(reservation)
                self.data_manager.save_reservations(reservations)
                
                # Remove tickets from purchase history
                user_history = self.user.get_purchase_history()
                tickets_to_remove = [t.get_ticket_id() for t in reservation.get_tickets()]
                user_history.set_tickets([t for t in user_history.get_tickets() if t.get_ticket_id() not in tickets_to_remove])
                
                self.load_reservations()
                messagebox.showinfo("Success", "Reservation cancelled successfully!")
    
    def new_reservation(self):
        """Create a new reservation."""
        from .ticket_gui import TicketsGUI
        ticket_window = tk.Toplevel(self.master)
        TicketsGUI(ticket_window, self.user) 
