"""
Payment class for the Grand Prix Experience ticket booking system.
"""
class Payment:
    def __init__(self, paymentID, amount, date, method):
        self.__paymentID = paymentID
        self.__amount = amount
        self.__date = date
        self.__method = method

    def getPaymentID(self): return self.__paymentID
    def setPaymentID(self, id): self.__paymentID = id

    def getAmount(self): return self.__amount
    def setAmount(self, amount): self.__amount = amount

    def getDate(self): return self.__date
    def setDate(self, date): self.__date = date

    def getMethod(self): return self.__method
    def setMethod(self, method): self.__method = method

    def processPayment(self):
        print(f"Processing {self.__method} payment of {self.__amount} AED")
