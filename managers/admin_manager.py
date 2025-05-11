class AdminManager:
    def __init__(self, admin):
        self.admin = admin

    def view_sales_data(self, tickets):
        return len(tickets)

    def manage_events(self, events):
        return events
