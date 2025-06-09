import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
from datetime import datetime


class UserRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def create_user(self, email, password, role="seeker"):
        """Create a new user"""
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
            conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def authenticate_user(self, email, password):
        """Authenticate user and return user data"""
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
            if conn:
                conn.close()

    def get_user_by_id(self, user_id):
        """Get user by ID"""
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
            if conn:
                conn.close()

    def update_profile(self, user_id, **kwargs):
        """Update user profile"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            # Build dynamic update query
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['display_name', 'bio', 'age', 'location', 'profile_photo']:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if fields:
                fields.append("updated_at = %s")
                values.append(datetime.now())
                values.append(user_id)
                
                query = f"UPDATE user_profiles SET {', '.join(fields)} WHERE user_id = %s"
                cur.execute(query, values)
                conn.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating profile: {e}")
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def change_password(self, user_id, new_password):
        """Change user password"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            cur.execute("""
                UPDATE users SET password_hash = %s, updated_at = %s
                WHERE id = %s
            """, (password_hash, datetime.now(), user_id))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error changing password: {e}")
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def get_user_stats(self, user_id):
        """Get user statistics"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get basic stats - simplified for now since other tables may not exist
            stats = {
                'total_bookings': 0,
                'pending_bookings': 0,
                'completed_bookings': 0,
                'total_spent': 0,
                'total_earnings': 0,
                'messages_count': 0
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {}
        finally:
            if conn:
                conn.close()


class EscortRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def get_escort_profiles(self, limit=10, offset=0):
        """Get escort profiles with pagination"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT u.id, u.email, p.display_name, p.bio, p.age, p.location, 
                       p.profile_photo, ep.hourly_rate, ep.services_offered as services, 
                       ep.is_available as availability, 0 as is_online, 
                       0 as average_rating, 0 as total_reviews
                FROM users u
                JOIN user_profiles p ON u.id = p.user_id
                LEFT JOIN escort_profiles ep ON u.id = ep.user_id
                WHERE u.role = 'escort' AND u.is_active = true
                ORDER BY p.display_name
                LIMIT %s OFFSET %s
            """, (limit, offset))
            
            profiles = cur.fetchall()
            return [dict(profile) for profile in profiles]
            
        except Exception as e:
            print(f"Error getting escort profiles: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_total_escort_count(self):
        """Get total number of active escorts"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT COUNT(*) FROM users 
                WHERE role = 'escort' AND is_active = true
            """)
            
            count = cur.fetchone()[0]
            return count
            
        except Exception as e:
            print(f"Error getting escort count: {e}")
            return 0
        finally:
            if conn:
                conn.close()


class BookingRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def create_booking(self, client_id, escort_id, booking_data):
        """Create a new booking"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO bookings (seeker_id, escort_id, booking_date, duration_hours,
                                    total_amount, special_requests, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                client_id, escort_id, booking_data['booking_date'],
                booking_data['duration_hours'], booking_data['total_amount'],
                booking_data.get('special_requests', ''), 'pending',
                datetime.now(), datetime.now()
            ))
            
            booking_id = cur.fetchone()[0]
            conn.commit()
            return booking_id
            
        except Exception as e:
            print(f"Error creating booking: {e}")
            conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def get_user_bookings(self, user_id, role='client'):
        """Get bookings for a user"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            if role == 'client':
                field = 'seeker_id'
            else:
                field = 'escort_id'
            
            cur.execute(f"""
                SELECT b.*, 
                       cp.display_name as client_name,
                       ep.display_name as escort_name
                FROM bookings b
                LEFT JOIN user_profiles cp ON b.seeker_id = cp.user_id
                LEFT JOIN user_profiles ep ON b.escort_id = ep.user_id
                WHERE b.{field} = %s
                ORDER BY b.booking_date DESC
            """, (user_id,))
            
            bookings = cur.fetchall()
            return [dict(booking) for booking in bookings]
            
        except Exception as e:
            print(f"Error getting bookings: {e}")
            return []
        finally:
            if conn:
                conn.close()


class MessageRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def send_message(self, sender_id, recipient_id, content):
        """Send a message"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO messages (sender_id, recipient_id, message_text, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (sender_id, recipient_id, content, datetime.now()))
            
            message_id = cur.fetchone()[0]
            conn.commit()
            return message_id
            
        except Exception as e:
            print(f"Error sending message: {e}")
            conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def get_conversations(self, user_id):
        """Get conversations for a user"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT DISTINCT 
                    CASE 
                        WHEN sender_id = %s THEN recipient_id 
                        ELSE sender_id 
                    END as other_user_id,
                    p.display_name as other_user_name,
                    p.profile_photo,
                    (SELECT message_text FROM messages m2 
                     WHERE (m2.sender_id = %s AND m2.recipient_id = other_user_id) 
                        OR (m2.sender_id = other_user_id AND m2.recipient_id = %s)
                     ORDER BY m2.created_at DESC LIMIT 1) as last_message,
                    (SELECT created_at FROM messages m2 
                     WHERE (m2.sender_id = %s AND m2.recipient_id = other_user_id) 
                        OR (m2.sender_id = other_user_id AND m2.recipient_id = %s)
                     ORDER BY m2.created_at DESC LIMIT 1) as last_message_time
                FROM messages m
                JOIN user_profiles p ON p.user_id = CASE 
                    WHEN m.sender_id = %s THEN m.recipient_id 
                    ELSE m.sender_id 
                END
                WHERE m.sender_id = %s OR m.recipient_id = %s
                ORDER BY last_message_time DESC
            """, (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id))
            
            conversations = cur.fetchall()
            return [dict(conv) for conv in conversations]
            
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []
        finally:
            if conn:
                conn.close()


class PaymentRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def create_payment(self, user_id, booking_id, amount, payment_type='payment'):
        """Create a payment record"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO payments (payer_id, booking_id, amount, status, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (user_id, booking_id, amount, 'completed', datetime.now()))
            
            payment_id = cur.fetchone()[0]
            conn.commit()
            return payment_id
            
        except Exception as e:
            print(f"Error creating payment: {e}")
            conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def get_user_payments(self, user_id):
        """Get payments for a user"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT p.*, b.booking_date, up.display_name as other_party
                FROM payments p
                LEFT JOIN bookings b ON p.booking_id = b.id
                LEFT JOIN user_profiles up ON up.user_id = CASE 
                    WHEN b.seeker_id = %s THEN b.escort_id 
                    ELSE b.seeker_id 
                END
                WHERE p.payer_id = %s
                ORDER BY p.created_at DESC
            """, (user_id, user_id))
            
            payments = cur.fetchall()
            return [dict(payment) for payment in payments]
            
        except Exception as e:
            print(f"Error getting payments: {e}")
            return []
        finally:
            if conn:
                conn.close()