
"""
Data paths for the Grand Prix Experience ticket booking system.
"""
import os

# Base directory
DATA_DIR = "data"

# Data files
USERS_FILE = os.path.join(DATA_DIR, "user.pickle")
VENUES_FILE = os.path.join(DATA_DIR, "venue.pickle")
EVENTS_FILE = os.path.join(DATA_DIR, "event.pickle")
TICKETS_FILE = os.path.join(DATA_DIR, "ticket.pickle")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservation.pickle")
PAYMENTS_FILE = os.path.join(DATA_DIR, "payment.pickle")
DISCOUNTS_FILE = os.path.join(DATA_DIR, "discount.pickle") 
