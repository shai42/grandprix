"""
Venue class for the Grand Prix Experience ticket booking system.
"""

class Venue:
    """Represents a racing venue in the Grand Prix Experience system."""
    
    def __init__(self, venue_id=0, location="", capacity=0):
        """Initialize a new Venue object"""
        self.__venue_id = venue_id
        self.__location = location
        self.__capacity = capacity
    
    def get_venue_id(self):
        """Get the venue's unique identifier."""
        return self.__venue_id
    
    def set_venue_id(self, id):
        """Set the venue's unique identifier."""
        self.__venue_id = id
    
    def get_location(self):
        """Get the venue's location."""
        return self.__location
    
    def set_location(self, location):
        """Set the venue's location."""
        self.__location = location
    
    def get_capacity(self):
        """Get the venue's total capacity."""
        return self.__capacity
    
    def set_capacity(self, capacity):
        """Set the venue's total capacity."""
        self.__capacity = capacity
    
    def track_capacity(self):
        """Track capacity changes when tickets are sold or returned."""
        print(f"Tracking capacity for venue: {self.__venue_id}")
        return True
