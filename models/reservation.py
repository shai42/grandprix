"""
Reservation class for the Grand Prix Experience ticket booking system.
"""
from datetime import datetime

class Reservation:
    def __init__(self, reservation_id=0, date=None):
        """Initialize a new Reservation object"""
        self.__reservation_id = reservation_id
        self.__date = date if date else datetime.now()
        self.__tickets = []  # Composition: Reservation contains tickets
    
    def get_reservation_id(self):
        """Get the reservation's unique identifier."""
        return self.__reservation_id
    
    def set_reservation_id(self, id):
        """Set the reservation's unique identifier."""
        self.__reservation_id = id
    
    def get_date(self):
        """Get the reservation's date."""
        return self.__date
    
    def set_date(self, date):
        """Set the reservation's date."""
        self.__date = date
    
    def confirm(self):
        """Confirm the reservation."""
        print(f"Reservation {self.__reservation_id} has been confirmed.")
        return True
    
    def cancel(self):
        """Cancel the reservation."""
        print(f"Reservation {self.__reservation_id} has been cancelled.")
        return True
    
    def generate_ticket(self):
        """Generate tickets for this reservation."""
        print(f"Generating tickets for reservation {self.__reservation_id}")
        return True
    
    def add_ticket(self, ticket):
        """Add a ticket to this reservation."""
        self.__tickets.append(ticket)
    
    def get_tickets(self):
        """Get all tickets for this reservation."""
        return self.__tickets
