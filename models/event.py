
"""
Event class for the Grand Prix Experience System.
"""
class Event:
    def __init__(self, eventID, name, date):
        self.__eventID = eventID
        self.__name = name
        self.__date = date

    def getEventID(self): return self.__eventID
    def setEventID(self, id): self.__eventID = id

    def getName(self): return self.__name
    def setName(self, name): self.__name = name

    def getDate(self): return self.__date
    def setDate(self, date): self.__date = date

    def getDetails(self):
        return f"Event: {self.__name} on {self.__date}"