from models.user import User

class Admin(User):
    def viewSalesData(self):
        print("Viewing sales data...")

    def manageEvents(self):
        print("Managing events...")