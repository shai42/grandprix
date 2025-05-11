import pickle
import os

ORDER_FILE = 'data/orders.pkl'

def save_order(order_data):
    if not os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, 'wb') as f:
            pickle.dump([], f)
    with open(ORDER_FILE, 'rb') as f:
        orders = pickle.load(f)
    orders.append(order_data)
    with open(ORDER_FILE, 'wb') as f:
        pickle.dump(orders, f)

def load_orders_by_user(email):
    if not os.path.exists(ORDER_FILE):
        return []
    with open(ORDER_FILE, 'rb') as f:
        orders = pickle.load(f)
    return [o for o in orders if o["user_email"] == email]

def delete_order(ticket_id, email):
    if not os.path.exists(ORDER_FILE):
        return
    with open(ORDER_FILE, 'rb') as f:
        orders = pickle.load(f)
    updated = [o for o in orders if not (o["ticket_id"] == ticket_id and o["user_email"] == email)]
    with open(ORDER_FILE, 'wb') as f:
        pickle.dump(updated, f)

