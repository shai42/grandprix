"""
Ticket class and subclasses for the Grand Prix Experience ticket booking system.
"""
class Ticket:
    def __init__(self, ticketID, price, issueDate):
        self.__ticketID = ticketID
        self.__price = price
        self.__issueDate = issueDate

    def getTicketID(self): return self.__ticketID
    def setTicketID(self, id): self.__ticketID = id

    def getPrice(self): return self.__price
    def setPrice(self, price): self.__price = price

    def getIssueDate(self): return self.__issueDate
    def setIssueDate(self, date): self.__issueDate = date

    def calculatePrice(self): return self.__price

class SingleRacePass(Ticket):
    def calculatePrice(self): return self.getPrice()

class WeekendPackage(Ticket):
    def calculatePrice(self): return self.getPrice() * 1.5

class SeasonMembership(Ticket):
    def calculatePrice(self): return self.getPrice() * 5

class GroupDiscount(Ticket):
    def calculatePrice(self): return self.getPrice() * 0.8