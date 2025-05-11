import tkinter as tk
from tkinter import messagebox
import pickle

class UserDashboard(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user  # The logged-in user
        
        self.create_widgets()

    def create_widgets(self):
        # Welcome message
        self.title_label = tk.Label(self, text=f"Welcome, {self.user.getName()}", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, columnspan=2)

        # View profile button
        self.view_profile_button = tk.Button(self, text="View Profile", command=self.view_profile)
        self.view_profile_button.grid(row=1, column=0, padx=10, pady=10)

        # Update profile button
        self.update_profile_button = tk.Button(self, text="Update Profile", command=self.update_profile)
        self.update_profile_button.grid(row=1, column=1, padx=10, pady=10)

        # View purchase history button
        self.view_history_button = tk.Button(self, text="View Purchase History", command=self.view_purchase_history)
        self.view_history_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Listbox for displaying purchase history
        self.purchase_listbox = tk.Listbox(self, width=50, height=10)
        self.purchase_listbox.grid(row=3, column=0, columnspan=2, pady=10)

        # Delete and Modify buttons
        self.delete_button = tk.Button(self, text="Delete Order", command=self.delete_order)
        self.delete_button.grid(row=4, column=0, padx=10, pady=10)

        self.modify_button = tk.Button(self, text="Modify Order", command=self.modify_order)
        self.modify_button.grid(row=4, column=1, padx=10, pady=10)

        # Load the purchase history when the dashboard is loaded
        self.load_purchase_history()

    def load_purchase_history(self):
        try:
            with open("tickets.pkl", "rb") as f:
                tickets = pickle.load(f)
                # Filter tickets by user ID and display them
                user_tickets = [ticket for ticket in tickets if ticket.getUserID() == self.user.getUserID()]
                self.purchase_listbox.delete(0, tk.END)
                for ticket in user_tickets:
                    self.purchase_listbox.insert(tk.END, f"Ticket {ticket.getTicketID()} - {ticket.getPrice()} USD")
        except FileNotFoundError:
            messagebox.showwarning("No Tickets", "No ticket data available.")

    def view_profile(self):
        profile_info = f"Name: {self.user.getName()}\nEmail: {self.user.getEmail()}"
        messagebox.showinfo("Profile Info", profile_info)

    def update_profile(self):
        update_window = tk.Toplevel(self)
        update_window.title("Update Profile")
        
        tk.Label(update_window, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, self.user.getName())
        name_entry.grid(row=0, column=1)

        tk.Label(update_window, text="Email:").grid(row=1, column=0)
        email_entry = tk.Entry(update_window)
        email_entry.insert(0, self.user.getEmail())
        email_entry.grid(row=1, column=1)

        def save_changes():
            self.user.setName(name_entry.get())
            self.user.setEmail(email_entry.get())

            # Save updated user data to the pickle file
            try:
                with open("users.pkl", "wb") as f:
                    pickle.dump(self.user, f)
                messagebox.showinfo("Profile Updated", "Your profile has been updated.")
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save profile: {str(e)}")

        save_button = tk.Button(update_window, text="Save Changes", command=save_changes)
        save_button.grid(row=2, column=0, columnspan=2)

    def delete_order(self):
        selected_ticket = self.purchase_listbox.curselection()
        if selected_ticket:
            ticket_id = selected_ticket[0]  # Get the ticket ID from the listbox
            # Delete the selected ticket from the pickle file
            try:
                with open("tickets.pkl", "rb") as f:
                    tickets = pickle.load(f)

                tickets = [ticket for ticket in tickets if ticket.getTicketID() != ticket_id]

                with open("tickets.pkl", "wb") as f:
                    pickle.dump(tickets, f)

                messagebox.showinfo("Order Deleted", f"Ticket {ticket_id} has been deleted.")
                self.load_purchase_history()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete order: {str(e)}")

    def modify_order(self):
        selected_ticket = self.purchase_listbox.curselection()
        if selected_ticket:
            ticket_id = selected_ticket[0]
            modify_window = tk.Toplevel(self)
            modify_window.title("Modify Order")

            # Modify logic (e.g., change ticket type or date)
            modify_button = tk.Button(modify_window, text="Modify", command=lambda: self.modify_ticket(ticket_id))
            modify_button.grid(row=1, column=0, columnspan=2)

    def modify_ticket(self, ticket_id):
        try:
            # Load tickets, find the one to modify
            with open("tickets.pkl", "rb") as f:
                tickets = pickle.load(f)

            ticket_to_modify = next((ticket for ticket in tickets if ticket.getTicketID() == ticket_id), None)
            if ticket_to_modify:
                # Modify ticket (e.g., change price or date)
                ticket_to_modify.setPrice(200)  # Example change, modify as needed

                # Save modified ticket list back to pickle file
                with open("tickets.pkl", "wb") as f:
                    pickle.dump(tickets, f)
                messagebox.showinfo("Ticket Modified", f"Ticket {ticket_id} has been modified.")
                self.load_purchase_history()
            else:
                messagebox.showwarning("Ticket Not Found", f"Ticket {ticket_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to modify ticket: {str(e)}")

