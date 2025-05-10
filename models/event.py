
"""
Event class for the Grand Prix Experience System.
"""
from datetime import datetime

class Event:
    """Represents a racing event in the Grand Prix Experience system."""
    def __init__(self, event_id=0, name="", date=None, venue_id=0):
        """Initialize a new Event object"""
        self.__event_id = event_id
        self.__name = name
        self.__date = date if date else datetime.now()
    def get_event_id(self):
        """Get the event's unique identifier."""
        return self.__event_id
    
    def set_event_id(self, id):
        """Set the event's unique identifier."""
        self.__event_id = id
    
    def get_name(self):
        """Get the event's name."""
        return self.__name
    
    def set_name(self, name):
        """Set the event's name."""
        self.__name = name
    
    def get_date(self):
        """Get the event's date and time."""
        return self.__date
    
    def set_date(self, date):
        """Set the event's date and time."""
        self.__date = date
    
    def get_details(self):
        """Get complete details about the event."""
        return f"Event: {self.__name} (ID: {self.__event_id}) on {self.__date.strftime('%Y-%m-%d')}" 
           