
"""
Discount class for the Grand Prix Experience ticket booking system.
"""

class Discount:
    def __init__(self, discountID, description, percentage):
        self.__discountID = discountID
        self.__description = description
        self.__percentage = percentage

    def getDiscountID(self): return self.__discountID
    def setDiscountID(self, id): self.__discountID = id

    def getDescription(self): return self.__description
    def setDescription(self, desc): self.__description = desc

    def getPercentage(self): return self.__percentage
    def setPercentage(self, perc): self.__percentage = perc

    def applyDiscount(self, amount):
        return amount * (1 - self.__percentage / 100)