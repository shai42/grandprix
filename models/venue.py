"""
Venue class for the Grand Prix Experience ticket booking system.
"""

class Venue:
    """Represents a racing venue in the Grand Prix Experience system."""
    def __init__(self, venue_id=0, location="", capacity=0, rows=10, seats_per_row=20):
        """Initialize a new Venue object"""
        self.__venue_id = venue_id
        self.__location = location
        self.__capacity = capacity
        self.__rows = rows
        self.__seats_per_row = seats_per_row
        self.__seats = self.__generate_seats(rows, seats_per_row)

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
    
    def get_rows(self):
        """Get the number of rows in the venue."""
        return self.__rows
    
    def set_rows(self, rows):
        """Set the number of rows in the venue."""
        self.__rows = rows
    
    def get_seats_per_row(self):
        """Get the number of seats per row."""
        return self.__seats_per_row
    
    def set_seats_per_row(self, seats_per_row):
        """Set the number of seats per row."""
        self.__seats_per_row = seats_per_row
    
    def track_capacity(self, tickets_sold: int) -> bool:
        """Track remaining capacity."""
        remaining = self.__capacity - tickets_sold
        print(f"Remaining capacity: {remaining}/{self.__capacity}")
        return remaining > 0  # True if seats available
    
    def __generate_seats(self, rows, seats_per_row):
        """Generate seats for the venue."""
        seats = {}
        for row in range(1, rows + 1):
            for num in range(1, seats_per_row + 1):
                seat_id = f"{chr(64 + row)}{num}"
                seats[seat_id] = Seat(seat_id, row, num)
        return seats
   
    def get_available_seats(self):
        """Get all available seats."""
        return [seat for seat in self.__seats.values() if not seat.is_reserved()]

class Seat:
    """Represents a seat in a venue."""
    def __init__(self, seat_id: str, row: int, number: int, is_reserved=False):
        """Initialize a new Seat object"""
        self.__seat_id = seat_id  # e.g., "A1", "B2"
        self.__row = row
        self.__number = number
        self.__is_reserved = is_reserved

    def get_seat_id(self):
        """Get the seat's unique identifier."""
        return self.__seat_id
    
    def set_seat_id(self, seat_id):
        """Set the seat's unique identifier."""
        self.__seat_id = seat_id
    
    def get_row(self):
        """Get the seat's row number."""
        return self.__row
    
    def set_row(self, row):
        """Set the seat's row number."""
        self.__row = row
    
    def get_number(self):
        """Get the seat's number."""
        return self.__number
    
    def set_number(self, number):
        """Set the seat's number."""
        self.__number = number
    
    def is_reserved(self):
        """Check if the seat is reserved."""
        return self.__is_reserved
    
    def reserve(self):
        """Reserve the seat."""
        self.__is_reserved = True
