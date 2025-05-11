"""
Admin dashboard for the Grand Prix Experience ticket booking system.
"""

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from models.discounts import Discount

class AdminDashboard:
    def __init__(self, master, admin):
        self.master = master
        self.admin = admin
        
        self.master.title(f"Grand Prix Experience - Admin Dashboard ({self.admin.get_name()})")
        self.master.geometry("800x600")
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create the admin dashboard widgets."""
        # Menu Bar
        menubar = tk.Menu(self.master)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Admin Menu
        admin_menu = tk.Menu(menubar, tearoff=0)
        admin_menu.add_command(label="Manage Events", command=self.manage_events)
        admin_menu.add_command(label="View Sales Data", command=self.view_sales_data)
        admin_menu.add_command(label="Manage Discounts", command=lambda: self.notebook.select(self.discounts_frame))
        menubar.add_cascade(label="Admin", menu=admin_menu)
        
        self.master.config(menu=menubar)
        
        # Main Frame
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Events Tab
        self.events_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.events_frame, text="Events")
        
        # Events Treeview
        self.events_tree = ttk.Treeview(self.events_frame, columns=("ID", "Name", "Date"), show="headings")
        self.events_tree.heading("ID", text="ID")
        self.events_tree.heading("Name", text="Name")
        self.events_tree.heading("Date", text="Date")
        self.events_tree.column("ID", width=50)
        self.events_tree.column("Name", width=200)
        self.events_tree.column("Date", width=150)
        self.events_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Events Buttons
        events_btn_frame = tk.Frame(self.events_frame)
        events_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(events_btn_frame, text="Add Event", command=self.add_event).pack(side=tk.LEFT, padx=5)
        tk.Button(events_btn_frame, text="Edit Event", command=self.edit_event).pack(side=tk.LEFT, padx=5)
        tk.Button(events_btn_frame, text="Delete Event", command=self.delete_event).pack(side=tk.LEFT, padx=5)
        
        # Sales Tab
        self.sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_frame, text="Sales")
        
        # Sales Treeview
        self.sales_tree = ttk.Treeview(self.sales_frame, columns=("Event", "Tickets Sold", "Revenue"), show="headings")
        self.sales_tree.heading("Event", text="Event")
        self.sales_tree.heading("Tickets Sold", text="Tickets Sold")
        self.sales_tree.heading("Revenue", text="Revenue")
        self.sales_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Discounts Tab (NEW)
        self.discounts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.discounts_frame, text="Discounts")
        
        # Discounts Treeview
        self.discounts_tree = ttk.Treeview(
            self.discounts_frame, 
            columns=("ID", "Description", "Percentage"), 
            show="headings"
        )
        self.discounts_tree.heading("ID", text="ID")
        self.discounts_tree.heading("Description", text="Description")
        self.discounts_tree.heading("Percentage", text="Percentage (%)")
        self.discounts_tree.column("ID", width=50)
        self.discounts_tree.column("Description", width=300)
        self.discounts_tree.column("Percentage", width=100)
        self.discounts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Discount Buttons
        discount_btn_frame = tk.Frame(self.discounts_frame)
        discount_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(discount_btn_frame, text="Add Discount", command=self.add_discount).pack(side=tk.LEFT, padx=5)
        tk.Button(discount_btn_frame, text="Edit Discount", command=self.edit_discount).pack(side=tk.LEFT, padx=5)
        tk.Button(discount_btn_frame, text="Delete Discount", command=self.delete_discount).pack(side=tk.LEFT, padx=5)
    
    def load_data(self):
        """Load data into the dashboard."""
        # Load events
        events = self.data_manager.load_events()
        for event in events:
            self.events_tree.insert("", tk.END, values=(
                event.get_event_id(),
                event.get_name(),
                event.get_date().strftime("%Y-%m-%d")
            ))
        
        # Load sales data (simplified)
        tickets = self.data_manager.load_tickets()
        sales_data = {}
        
        for ticket in tickets:
            event_id = getattr(ticket, "_Ticket__event_id", None)
            if event_id:
                if event_id not in sales_data:
                    sales_data[event_id] = {"count": 0, "revenue": 0}
                sales_data[event_id]["count"] += 1
                sales_data[event_id]["revenue"] += ticket.get_price()
        
        for event_id, data in sales_data.items():
            self.sales_tree.insert("", tk.END, values=(
                f"Event {event_id}",
                data["count"],
                f"${data['revenue']:.2f}"
            ))
        
        # Load discounts (NEW)
        discounts = self.data_manager.load_discounts() or []
        for discount in discounts:
            self.discounts_tree.insert("", tk.END, values=(
                discount.get_discount_id(),
                discount.get_description(),
                f"{discount.get_percentage() * 100:.1f}%"
            ))

    #Discount Management Methods
    def add_discount(self):
        """Open window to add a new discount."""
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Discount")
        add_window.geometry("400x250")
        
        tk.Label(add_window, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(add_window, width=40)
        desc_entry.pack(pady=5)
        
        tk.Label(add_window, text="Percentage (0-100):").pack(pady=5)
        perc_entry = tk.Entry(add_window, width=40)
        perc_entry.pack(pady=5)
        
        def save_discount():
            description = desc_entry.get()
            percentage = perc_entry.get()
            
            if not description or not percentage:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            try:
                percentage = float(percentage) / 100  # Convert to decimal
                if not (0 <= percentage <= 1):
                    raise ValueError("Percentage must be between 0 and 100")
                
                discounts = self.data_manager.load_discounts() or []
                new_id = max(d.get_discount_id() for d in discounts) + 1 if discounts else 1
                
                new_discount = Discount(new_id, description, percentage)
                discounts.append(new_discount)
                self.data_manager.save_discounts(discounts)
                
                self.discounts_tree.insert("", tk.END, values=(
                    new_id, description, f"{percentage * 100:.1f}%"
                ))
                add_window.destroy()
                messagebox.showinfo("Success", "Discount added successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(add_window, text="Save", command=save_discount).pack(pady=10)
    
    def edit_discount(self):
        """Edit selected discount."""
        selected = self.discounts_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a discount to edit")
            return
        
        item = self.discounts_tree.item(selected[0])
        discount_id, description, percentage = item["values"]
        
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Discount")
        edit_window.geometry("400x250")
        
        tk.Label(edit_window, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(edit_window, width=40)
        desc_entry.insert(0, description)
        desc_entry.pack(pady=5)
        
        tk.Label(edit_window, text="Percentage (0-100):").pack(pady=5)
        perc_entry = tk.Entry(edit_window, width=40)
        perc_entry.insert(0, percentage.replace("%", ""))
        perc_entry.pack(pady=5)
        
        def save_changes():
            new_desc = desc_entry.get()
            new_perc = perc_entry.get()
            
            if not new_desc or not new_perc:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            try:
                new_perc = float(new_perc) / 100
                if not (0 <= new_perc <= 1):
                    raise ValueError("Percentage must be between 0 and 100")
                
                discounts = self.data_manager.load_discounts() or []
                for discount in discounts:
                    if discount.get_discount_id() == int(discount_id):
                        discount.set_description(new_desc)
                        discount.set_percentage(new_perc)
                        break
                
                self.data_manager.save_discounts(discounts)
                self.discounts_tree.item(selected[0], values=(
                    discount_id, new_desc, f"{new_perc * 100:.1f}%"
                ))
                edit_window.destroy()
                messagebox.showinfo("Success", "Discount updated successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
    
    def delete_discount(self):
        """Delete selected discount."""
        selected = self.discounts_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a discount to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this discount?"):
            item = self.discounts_tree.item(selected[0])
            discount_id = item["values"][0]
            
            discounts = self.data_manager.load_discounts() or []
            discounts = [d for d in discounts if d.get_discount_id() != int(discount_id)]
            self.data_manager.save_discounts(discounts)
            
            self.discounts_tree.delete(selected[0])
            messagebox.showinfo("Success", "Discount deleted successfully!")

    # ===== EXISTING METHODS =====
    def manage_events(self):
        """Manage events."""
        self.notebook.select(self.events_frame)
    
    def view_sales_data(self):
        """View sales data."""
        self.notebook.select(self.sales_frame)
    
    def add_event(self):
        """Add a new event."""
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Event")
        add_window.geometry("400x250")
        
        tk.Label(add_window, text="Event Name:").pack(pady=5)
        name_entry = tk.Entry(add_window, width=40)
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Event Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(add_window, width=40)
        date_entry.pack(pady=5)
        
        def save_event():
            name = name_entry.get()
            date_str = date_entry.get()
            
            if not name or not date_str:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            try:
                from datetime import datetime
                date = datetime.strptime(date_str, "%Y-%m-%d")
                
                events = self.data_manager.load_events()
                new_id = max(e.get_event_id() for e in events) + 1 if events else 1
                
                from models.event import Event
                new_event = Event(event_id=new_id, name=name, date=date)
                events.append(new_event)
                self.data_manager.save_events(events)
                
                self.events_tree.insert("", tk.END, values=(new_id, name, date_str))
                add_window.destroy()
                messagebox.showinfo("Success", "Event added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        
        tk.Button(add_window, text="Save", command=save_event).pack(pady=10)
    
    def edit_event(self):
        """Edit selected event."""
        selected = self.events_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an event to edit")
            return
        
        item = self.events_tree.item(selected[0])
        event_id, name, date = item["values"]
        
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Event")
        edit_window.geometry("400x250")
        
        tk.Label(edit_window, text="Event Name:").pack(pady=5)
        name_entry = tk.Entry(edit_window, width=40)
        name_entry.insert(0, name)
        name_entry.pack(pady=5)
        
        tk.Label(edit_window, text="Event Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(edit_window, width=40)
        date_entry.insert(0, date)
        date_entry.pack(pady=5)
        
        def save_changes():
            new_name = name_entry.get()
            new_date_str = date_entry.get()
            
            if not new_name or not new_date_str:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            try:
                from datetime import datetime
                new_date = datetime.strptime(new_date_str, "%Y-%m-%d")
                
                events = self.data_manager.load_events()
                for event in events:
                    if event.get_event_id() == event_id:
                        event.set_name(new_name)
                        event.set_date(new_date)
                        break
                
                self.data_manager.save_events(events)
                
                self.events_tree.item(selected[0], values=(event_id, new_name, new_date_str))
                edit_window.destroy()
                messagebox.showinfo("Success", "Event updated successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        
        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
    
    def delete_event(self):
        """Delete selected event."""
        selected = self.events_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an event to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this event?"):
            item = self.events_tree.item(selected[0])
            event_id = item["values"][0]
            
            events = self.data_manager.load_events()
            events = [e for e in events if e.get_event_id() != event_id]
            self.data_manager.save_events(events)
            
            self.events_tree.delete(selected[0])
            messagebox.showinfo("Success", "Event deleted successfully!") 