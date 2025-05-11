"""
Reservation class for the Grand Prix Experience ticket booking system.
"""
from datetime import date

class Reservation:
    def __init__(self, reservationID, date):
        self.__reservationID = reservationID
        self.__date = date
        self.ticket = None
        self.seats = []

    def getReservationID(self): return self.__reservationID
    def setReservationID(self, id): self.__reservationID = id

    def getDate(self): return self.__date
    def setDate(self, date): self.__date = date

    def confirm(self): print("Reservation confirmed")
    def cancel(self): print("Reservation canceled")
    def generateTicket(self, ticket): self.ticket = ticket

    def addSeat(self, seat):
        if not seat.isReserved():
            seat.reserve()
            self.seats.append(seat)