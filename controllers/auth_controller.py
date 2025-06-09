from data_sources.repositories import UserRepository


class AuthController:
    def __init__(self, db_connector):
        self.user_repo = UserRepository(db_connector)

    def authenticate(self, email, password):
        """Authenticate user and return user data"""
        return self.user_repo.authenticate_user(email, password)

    def register(self, email, password, role="seeker"):
        """Register a new user"""
        user_id = self.user_repo.create_user(email, password, role)
        return user_id is not None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.user_repo.get_user_by_id(user_id)
    
    def update_profile(self, user_id, **kwargs):
        """Update user profile"""
        return self.user_repo.update_profile(user_id, **kwargs)
    
    def change_password(self, user_id, new_password):
        """Change user password"""
        return self.user_repo.change_password(user_id, new_password)
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        return self.user_repo.get_user_stats(user_id)

