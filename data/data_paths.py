
"""
Data paths for the Grand Prix Experience ticket booking system.
"""
import os

# Base directory
DATA_DIR = "data"

# Data files
USERS_FILE = os.path.join(DATA_DIR, "users.pickle")
VENUES_FILE = os.path.join(DATA_DIR, "venues.pickle")
EVENTS_FILE = os.path.join(DATA_DIR, "events.pickle")
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.pickle")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.pickle")
PAYMENTS_FILE = os.path.join(DATA_DIR, "payments.pickle")
DISCOUNTS_FILE = os.path.join(DATA_DIR, "discounts.pickle") 
