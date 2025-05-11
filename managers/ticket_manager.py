from data.tickets import TICKETS_FILE
from utils.file_handler import load_data, save_data

class TicketManager:
    def __init__(self):
        self.tickets = load_data(TICKETS_FILE)

    def generate_ticket(self, ticket):
        self.tickets.append(ticket)
        save_data(TICKETS_FILE, self.tickets)

    def get_all_tickets(self):
        return self.tickets
