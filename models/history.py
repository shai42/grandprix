"""
PurchaseHistory class for the Grand Prix Experience ticket booking system.
"""

class PurchaseHistory:
    def __init__(self, historyID):
        self.__historyID = historyID
        self.tickets = []

    def getHistoryID(self): return self.__historyID
    def setHistoryID(self, id): self.__historyID = id

    def getTickets(self): return self.tickets
    def setTickets(self, tickets): self.tickets = tickets

    def getHistory(self): return self.tickets