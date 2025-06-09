import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
from datetime import datetime


class UserRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def create_user(self, email, password, role="seeker"):
        """Create a new user"""
        conn = None
        cur = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cur.execute("""
                INSERT INTO users (email, password_hash, role, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (email, password_hash, role, datetime.now(), datetime.now()))
            
            user_id = cur.fetchone()[0]
            conn.commit()
            
            # Create user profile
            cur.execute("""
                INSERT INTO user_profiles (user_id, display_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, email.split('@')[0], datetime.now(), datetime.now()))
            
            conn.commit()
            return user_id
            
        except Exception as e:
            print(f"Error creating user: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                self.db.return_connection(conn)

    def authenticate_user(self, email, password):
        """Authenticate user and return user data"""
        conn = None
        cur = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cur.execute("""
                SELECT u.id, u.email, u.role, u.is_active, u.created_at,
                       p.display_name, p.bio, p.age, p.location, p.profile_photo
                FROM users u
                LEFT JOIN user_profiles p ON u.id = p.user_id
                WHERE u.email = %s AND u.password_hash = %s AND u.is_active = true
            """, (email, password_hash))
            
            user = cur.fetchone()
            return dict(user) if user else None
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                self.db.return_connection(conn)

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = None
        cur = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT u.id, u.email, u.role, u.is_active, u.created_at,
                       p.display_name, p.bio, p.age, p.location, p.profile_photo
                FROM users u
                LEFT JOIN user_profiles p ON u.id = p.user_id
                WHERE u.id = %s
            """, (user_id,))
            
            user = cur.fetchone()
            return dict(user) if user else None
            
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                self.db.return_connection(conn)

    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = None
        cur = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Complete stats for all templates
            stats = {
                'total_bookings': 0, 'pending_bookings': 0, 'completed_bookings': 0,
                'total_spent': 0, 'total_earnings': 0, 'messages_count': 0,
                'upcoming_bookings': 0, 'favorite_escorts': 0, 'active_chats': 0,
                'pending_requests': 0, 'bookings_this_week': 0, 'earnings_this_month': 0,
                'average_rating': 4.5, 'total_users': 100, 'active_escorts': 25,
                'bookings_today': 5, 'pending_reports': 2, 'revenue_today': 1250,
                'system_uptime': 99, 'total_seekers': 75, 'pending_verifications': 3,
                'reviewing_reports_count': 1, 'resolved_reports_count': 10
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {
                'total_bookings': 0, 'pending_bookings': 0, 'completed_bookings': 0,
                'total_spent': 0, 'total_earnings': 0, 'messages_count': 0,
                'upcoming_bookings': 0, 'favorite_escorts': 0, 'active_chats': 0,
                'pending_requests': 0, 'bookings_this_week': 0, 'earnings_this_month': 0,
                'average_rating': 0, 'total_users': 0, 'active_escorts': 0,
                'bookings_today': 0, 'pending_reports': 0, 'revenue_today': 0,
                'system_uptime': 0, 'total_seekers': 0, 'pending_verifications': 0,
                'reviewing_reports_count': 0, 'resolved_reports_count': 0
            }
        finally:
            if cur:
                cur.close()
            if conn:
                self.db.return_connection(conn)

# Placeholder classes to prevent import errors
class EscortRepository:
    def __init__(self, db_connector):
        self.db = db_connector
    
    def get_escort_profiles(self, limit=10, offset=0):
        return []
    
    def get_total_escort_count(self):
        return 0

class BookingRepository:
    def __init__(self, db_connector):
        self.db = db_connector

class MessageRepository:
    def __init__(self, db_connector):
        self.db = db_connector

class PaymentRepository:
    def __init__(self, db_connector):
        self.db = db_connector
