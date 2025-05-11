from data.users import USERS_FILE
from utils.file_handler import load_data, save_data

class UserManager:
    def __init__(self):
        self.users = load_data(USERS_FILE)

    def register_user(self, user):
        self.users.append(user)
        save_data(USERS_FILE, self.users)

    def login(self, email, password):
        for user in self.users:
            if user.getEmail() == email and user.getPassword() == password:
                return user
        return None

    def delete_user(self, userID):
        self.users = [u for u in self.users if u.getUserID() != userID]
        save_data(USERS_FILE, self.users)
