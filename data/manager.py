"""
Data manager for the Grand Prix Experience ticket booking system.
Handles loading and saving data using Pickle.
"""
import os
import pickle
from typing import Any, Dict, List

class DataManager:
    """Manages data persistence for the application."""
    
    def __init__(self, data_dir="data"):
        """Initialize the data manager."""
        self.data_dir = data_dir
        # Ensure the data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def save_object(self, obj: Any, filename: str) -> bool:
        """
        Save an object to a pickle file.
        
        Args:
            obj: The object to save
            filename: The name of the file to save to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(os.path.join(self.data_dir, filename), 'wb') as file:
                pickle.dump(obj, file)
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
    
    def load_object(self, filename: str) -> Any:
        """
        Load an object from a pickle file.
        
        Args:
            filename: The name of the file to load from
            
        Returns:
            Any: The loaded object, or None if there was an error
        """
        try:
            with open(os.path.join(self.data_dir, filename), 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error loading from {filename}: {e}")
            return None
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            filename: The name of the file to check
            
        Returns:
            bool: True if the file exists, False otherwise
        """
        return os.path.exists(os.path.join(self.data_dir, filename))
    
    # Additional methods for specific objects
    
    def save_users(self, users: List) -> bool:
        """Save the list of users."""
        return self.save_object(users, "users.pickle")
    
    def load_users(self) -> List:
        """Load the list of users."""
        return self.load_object("users.pickle") or []
    
    def save_venues(self, venues: List) -> bool:
        """Save the list of venues."""
        return self.save_object(venues, "venues.pickle")
    
    def load_venues(self) -> List:
        """Load the list of venues."""
        return self.load_object("venues.pickle") or []
    
    def save_events(self, events: List) -> bool:
        """Save the list of events."""
        return self.save_object(events, "events.pickle")
    
    def load_events(self) -> List:
        """Load the list of events."""
        return self.load_object("events.pickle") or []
    
    def save_tickets(self, tickets: List) -> bool:
        """Save the list of tickets."""
        return self.save_object(tickets, "tickets.pickle")
    
    def load_tickets(self) -> List:
        """Load the list of tickets."""
        return self.load_object("tickets.pickle") or []
    
    def save_reservations(self, reservations: List) -> bool:
        """Save the list of reservations."""
        return self.save_object(reservations, "reservations.pickle")
    
    def load_reservations(self) -> List:
        """Load the list of reservations."""
        return self.load_object("reservations.pickle") or []
    
    def save_payments(self, payments: List) -> bool:
        """Save the list of payments."""
        return self.save_object(payments, "payments.pickle")
    
    def load_payments(self) -> List:
        """Load the list of payments."""
        return self.load_object("payments.pickle") or []
