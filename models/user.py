"""
User class for the Grand Prix Experience ticket booking system.
"""

import pickle

class User:
    def __init__(self, userID, name, email, password):
        self.__userID = userID
        self.__name = name
        self.__email = email
        self.__password = password

    def getUserID(self): return self.__userID
    def setUserID(self, id): self.__userID = id

    def getName(self): return self.__name
    def setName(self, name): self.__name = name

    def getEmail(self): return self.__email
    def setEmail(self, email): self.__email = email

    def getPassword(self): return self.__password
    def setPassword(self, password): self.__password = password

    def login(self, email, password):
        return self.__email == email and self.__password == password

    def viewHistory(self):
        if hasattr(self, 'purchase_history'):
            return self.purchase_history.getHistory()
        return []

    def updateVisit(self):
        print("Visit updated for user", self.__name)

    def makeReservation(self, reservation):
        self.reservation = reservation

