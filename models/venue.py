"""
Venue class for the Grand Prix Experience ticket booking system.
"""

from models.seat import Seat

class Venue:
    def __init__(self, venueID, location, capacity):
        self.__venueID = venueID
        self.__location = location
        self.__capacity = capacity
        self.rows = 0
        self.seats_per_row = 0
        self.seats = []

    def getVenueID(self): return self.__venueID
    def setVenueID(self, id): self.__venueID = id

    def getLocation(self): return self.__location
    def setLocation(self, location): self.__location = location

    def getCapacity(self): return self.__capacity
    def setCapacity(self, capacity): self.__capacity = capacity

    def getRows(self): return self.rows
    def setRows(self, rows): self.rows = rows

    def getSeatsPerRow(self): return self.seats_per_row
    def setSeatsPerRow(self, seatsPerRow):
        self.seats_per_row = seatsPerRow
        self.generateSeats()

    def generateSeats(self):
        self.seats = []
        for r in range(self.rows):
            for s in range(self.seats_per_row):
                seatID = f"R{r+1}S{s+1}"
                self.seats.append(Seat(seatID, r+1, s+1))

    def getSeat(self, seatID):
        for seat in self.seats:
            if seat.getSeatID() == seatID:
                return seat
        return None

    def getAvailableSeats(self):
        return [seat for seat in self.seats if not seat.isReserved()]

    def trackCapacity(self):
        return len(self.getAvailableSeats()) < self.__capacity