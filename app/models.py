import secrets
import datetime

INITIAL_CREDITS = 10


class User: 
    def __init__(self):
        self.users = {}  
        self.user_id_counter = 1

    def add_user(self, username, password):
        if username in self.users.values():
            raise ValueError("Username already exists")
        
        user_id = self.user_id_counter
        self.user_id_counter += 1
        
        user = {
            "id": user_id,
            "username": username,
            "password": password,
            "api_key": self.generate_api_key(),
            "is_active": True,
            "created_at": datetime.datetime.now(),
            "credits": INITIAL_CREDITS
        }
        
        self.users[username] = user
        return user

    def get_user_by_username(self, username):
        return self.users.get(username)

    def get_user_by_api_key(self, api_key):
        for user in list(self.users.values()):
            if user["api_key"] == api_key:
                return user
        return False    
    
    def get_all_users(self):
        return list(self.users.values())

    def update_user(self, username, update_data):
        if username not in self.users.values():
            raise ValueError("User not found")
        
        for key, value in update_data.items():
            if key in self.users[username] and key != "id": 
                self.users[username][key] = value
                
        return self.users[username]

    def update_user_credits(self, username):
        if username not in self.users.values():
            raise ValueError("User not found")
        
        self.users[username]["credits"] -= 1
        return self.users[username]["credits"]

    def generate_api_key(self):
        return secrets.token_urlsafe(16)
        
    def delete_user(self, username):
        if username not in self.users.values():
            raise ValueError("User not found")
        
        del self.users[username]
        return True        

