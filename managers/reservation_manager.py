from data.reservations import RESERVATIONS_FILE
from utils.file_handler import load_data, save_data

class ReservationManager:
    def __init__(self):
        self.reservations = load_data(RESERVATIONS_FILE)

    def create_reservation(self, reservation):
        self.reservations.append(reservation)
        save_data(RESERVATIONS_FILE, self.reservations)

    def cancel_reservation(self, reservationID):
        self.reservations = [r for r in self.reservations if r.getReservationID() != reservationID]
        save_data(RESERVATIONS_FILE, self.reservations)

    def get_all_reservations(self):
        return self.reservations
