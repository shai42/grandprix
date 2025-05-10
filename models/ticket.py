"""
Ticket class and subclasses for the Grand Prix Experience ticket booking system.
"""
from datetime import datetime

class Ticket:
    def __init__(self, ticket_id=0, price=0.0, issue_date=None):
        """Initialize a new Ticket object"""
        self.__ticket_id = ticket_id
        self.__price = price
        self.__issue_date = issue_date if issue_date else datetime.now()
        self.__discount = None  #Association: Ticket may have a Discount
    
    def get_ticket_id(self):
        """Get the ticket's unique identifier."""
        return self.__ticket_id
    
    def set_ticket_id(self, id):
        """Set the ticket's unique identifier."""
        self.__ticket_id = id
    
    def get_price(self):
        """Get the ticket's price."""
        return self.__price
    
    def set_price(self, price):
        """Set the ticket's price."""
        self.__price = price
    
    def get_issue_date(self):
        """Get the ticket's issue date."""
        return self.__issue_date
    
    def set_issue_date(self, date):
        """Set the ticket's issue date."""
        self.__issue_date = date
    
    def calculate_price(self):
        """Calculate the ticket's price."""
        if self.__discount:
            return self.__price - (self.__price * self.__discount.get_percentage())
        return self.__price
    
    def set_discount(self, discount):
        """Set the discount for this ticket."""
        self.__discount = discount
    
    def get_discount(self):
        """Get the discount for this ticket."""
        return self.__discount


class SingleRacePass(Ticket):
    """Single race pass ticket type."""
    
    def __init__(self, ticket_id=0, price=0.0, issue_date=None, event_id=0):
        """Initialize a new SingleRacePass object"""
        super().__init__(ticket_id, price, issue_date)
        self.__event_id = event_id
    
    def calculate_price(self):
        """Calculate the price for a single race pass."""
        base_price = super().calculate_price()
        return base_price  


class WeekendPackage(Ticket):
    """Weekend package ticket type."""
    
    def __init__(self, ticket_id=0, price=0.0, issue_date=None, weekend_id=0):
        """Initialize a new WeekendPackage object"""
        super().__init__(ticket_id, price, issue_date)
        self.__weekend_id = weekend_id
        self.__events_included = []  # List of event IDs included in this package
    
    def calculate_price(self):
        """Calculate the price for a weekend package."""
        base_price = super().calculate_price()
        # Apply a 10% package discount
        return base_price * 0.9
    
    def add_event(self, event_id):
        """Add an event to this weekend package."""
        self.__events_included.append(event_id)


class SeasonMembership(Ticket):
    """Season membership ticket type."""
    
    def __init__(self, ticket_id=0, price=0.0, issue_date=None, season_year=None):
        """Initialize a new SeasonMembership object"""
        super().__init__(ticket_id, price, issue_date)
        self.__season_year = season_year if season_year else datetime.now().year
        self.__perks = []  # List of perks included with this membership
    
    def calculate_price(self):
        """Calculate the price for a season membership."""
        base_price = super().calculate_price()
        # Apply a 25% season discount
        return base_price * 0.75
    
    def add_perk(self, perk):
        """Add a perk to this season membership."""
        self.__perks.append(perk)


class GroupDiscount(Ticket):
    """Group discount ticket type."""
    
    def __init__(self, ticket_id=0, price=0.0, issue_date=None, group_size=1):
        """Initialize a new GroupDiscount object"""
        super().__init__(ticket_id, price, issue_date)
        self.__group_size = group_size
    
    def calculate_price(self):
        """Calculate the price for a group discount ticket."""
        base_price = super().calculate_price()
        # Calculate discount based on group size
        if self.__group_size >= 10:
            return base_price * 0.7  # 30% discount for 10+ people
        elif self.__group_size >= 5:
            return base_price * 0.8  # 20% discount for 5-9 people
        else:
            return base_price * 0.9  # 10% discount for 2-4 people
