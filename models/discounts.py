
"""
Discount class for the Grand Prix Experience ticket booking system.
"""

class Discount:
    def __init__(self, discount_id=0, description="", percentage=0.0):
        """Initialize a new Discount object"""
        self.__discount_id = discount_id
        self.__description = description
        self.__percentage = percentage
    
    def get_discount_id(self):
        """Get the discount's unique identifier."""
        return self.__discount_id
    
    def set_discount_id(self, id):
        """Set the discount's unique identifier."""
        self.__discount_id = id
    
    def get_description(self):
        """Get the discount's description."""
        return self.__description
    
    def set_description(self, description):
        """Set the discount's description."""
        self.__description = description
    
    def get_percentage(self):
        """Get the discount percentage."""
        return self.__percentage
    
    def set_percentage(self, percentage):
        """Set the discount percentage."""
        if 0 <= percentage <= 1:
            self.__percentage = percentage
        else:
            raise ValueError("Discount percentage must be between 0 and 1")
    
    def apply_discount(self):
        """Apply the discount."""
        return self.__percentage 
