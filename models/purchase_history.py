"""
PurchaseHistory class for the Grand Prix Experience ticket booking system.
"""

class PurchaseHistory:
    def __init__(self, history_id=0):
        """Initialize a new PurchaseHistory object"""
        self.__history_id = history_id
        self.__tickets = []  # Aggregation: PurchaseHistory is related to Tickets
    
    def get_history_id(self):
        """Get the history's unique identifier."""
        return self.__history_id
    
    def set_history_id(self, id):
        """Set the history's unique identifier."""
        self.__history_id = id
    
    def get_tickets(self):
        """Get all tickets in this purchase history."""
        return self.__tickets
    
    def set_tickets(self, tickets):
        """Set all tickets in this purchase history."""
        self.__tickets = tickets
    
    def get_history(self):
        """Get the purchase history as a list of tickets."""
        return self.__tickets
    
    def add_ticket(self, ticket):
        """Add a ticket to the purchase history."""
        self.__tickets.append(ticket)
