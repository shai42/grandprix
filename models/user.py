"""
User class for the Grand Prix Experience ticket booking system.
"""
from models.purchase_history import PurchaseHistory

class User:
    def __init__(self, user_id=0, name="", email="", password=""):
        """Initialize a new User object"""
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__purchase_history = PurchaseHistory()  # Composition: User has a PurchaseHistory
    
    def get_user_id(self):
        """Get the user's unique identifier."""
        return self.__user_id
    
    def set_user_id(self, id):
        """Set the user's unique identifier."""
        self.__user_id = id
    
    def get_name(self):
        """Get the user's name."""
        return self.__name
    
    def set_name(self, name):
        """Set the user's name."""
        self.__name = name
    
    def get_email(self):
        """Get the user's email."""
        return self.__email
    
    def set_email(self, email):
        """Set the user's email."""
        self.__email = email
    
    def get_password(self):
        """Get the user's password."""
        return self.__password
    
    def set_password(self, password):
        """Set the user's password."""
        self.__password = password
    
    def login(self):
        """Login the user."""
        print(f"User {self.__user_id} ({self.__email}) logged in.")
        return True
    
    def view_history(self):
        """View the user's purchase history."""
        return self.__purchase_history.get_history()
    
    def update_visit(self):
        """Update the user's visit information."""
        print(f"Visit information updated for user {self.__user_id}")
        return True
    
    def make_reservation(self):
        """Make a new reservation."""
        print(f"Creating reservation for user {self.__user_id}")
        # In a real implementation, would create and return a Reservation object
        return True
    
    def get_purchase_history(self):
        """Get the user's purchase history."""
        return self.__purchase_history


class Admin(User):
    """Admin class inherits from User."""
    
    def __init__(self, user_id=0, name="", email="", password=""):
        """Initialize a new Admin object"""
        super().__init__(user_id, name, email, password)
    
    def view_sales_data(self):
        """View sales data."""
        print("Viewing sales data (Admin function)")
        return True
    
    def manage_events(self):
        """Manage events."""
        print("Managing events (Admin function)")
        return True
    
