"""
Payment class for the Grand Prix Experience ticket booking system.
"""
from datetime import datetime

class Payment:
    def __init__(self, payment_id=0, amount=0.0, date=None, method=""):
        """Initialize a new Payment object"""
        self.__payment_id = payment_id
        self.__amount = amount
        self.__date = date if date else datetime.now()
        self.__method = method
        self.__tickets = []  # Association: Payment covers tickets
    
    def get_payment_id(self):
        """Get the payment's unique identifier."""
        return self.__payment_id
    
    def set_payment_id(self, id):
        """Set the payment's unique identifier."""
        self.__payment_id = id
    
    def get_amount(self):
        """Get the payment amount."""
        return self.__amount
    
    def set_amount(self, amount):
        """Set the payment amount."""
        self.__amount = amount
    
    def get_date(self):
        """Get the payment date."""
        return self.__date
    
    def set_date(self, date):
        """Set the payment date."""
        self.__date = date
    
    def get_method(self):
        """Get the payment method."""
        return self.__method
    
    def set_method(self, method):
        """Set the payment method."""
        self.__method = method
    
    def process_payment(self):
        """Process the payment."""
        print(f"Processing payment {self.__payment_id} for {self.__amount} via {self.__method}")
        # In a real implementation, would handle payment processing logic
        return True
    
    def add_ticket(self, ticket):
        """Add a ticket to this payment."""
        self.__tickets.append(ticket)
    
    def get_tickets(self):
        """Get all tickets covered by this payment."""
        return self.__tickets
