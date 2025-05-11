class Seat:
    def __init__(self, seatID, row, number):
        self.__seatID = seatID
        self.row = row
        self.number = number
        self.reserved = False

    def getSeatID(self): return self.__seatID
    def setSeatID(self, seatID): self.__seatID = seatID

    def reserve(self): self.reserved = True
    def isReserved(self): return self.reserved
