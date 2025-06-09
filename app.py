from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from db import PostgresConnector
import secrets
import os

from controllers.auth_controller import AuthController
from data_sources.repositories import EscortRepository, BookingRepository

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Validate required environment variables
required_vars = [
    "DATABASE_HOST",
    "DATABASE_PORT",
    "DATABASE_NAME",
    "DATABASE_USERNAME",
    "DATABASE_PASSWORD",
]
for var in required_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Log non-sensitive vars in development
if os.environ.get("FLASK_ENV") == "development":
    print(f"[INFO] Connecting to DB host: {os.environ['DATABASE_HOST']}")
    print(f"[INFO] DB port: {os.environ['DATABASE_PORT']}")
    print(f"[INFO] DB name: {os.environ['DATABASE_NAME']}")

# Persistent DB connector
db = PostgresConnector(
    host=os.environ["DATABASE_HOST"],
    port=int(os.environ["DATABASE_PORT"]),
    database=os.environ["DATABASE_NAME"],
    user=os.environ["DATABASE_USERNAME"],
    password=os.environ["DATABASE_PASSWORD"],
)

auth_controller = AuthController(db)

def get_db_conn():
    if "db_conn" not in g:
        g.db_conn = db.get_connection()
    return g.db_conn

@app.teardown_appcontext
def close_db_conn(exception):
    conn = g.pop("db_conn", None)
    if conn:
        db.return_connection(conn)

@app.route("/")
@app.route("/home")
def index():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
    except Exception:
        version = "Unavailable"
    return render_template("index.html", version=version)

@app.route("/auth", methods=["GET", "POST"])
def auth_page():
    """Unified authentication page for login and registration"""
    if request.method == "POST":
        action = request.form.get("action", "login")
        
        if action == "login":
            email = request.form.get("email")
            password = request.form.get("password")
            user = auth_controller.authenticate(email, password)
            if user:
                session['user_id'] = user.get('id')
                session['user_email'] = user.get('email')
                session['user_role'] = user.get('role', 'seeker')
                flash("Login successful!", "success")
                return redirect(url_for("dashboard_page"))
            flash("Invalid email or password", "danger")
            
        elif action == "register":
            email = request.form.get("email")
            pwd = request.form.get("password")
            cpwd = request.form.get("confirm_password")
            role = request.form.get("role", "seeker")
            
            if pwd != cpwd:
                flash("Passwords do not match", "danger")
            elif auth_controller.register(email, pwd, role):
                flash("Account created successfully! Please log in.", "success")
                return redirect(url_for("auth_page"))
            else:
                flash("Email already registered or registration failed", "danger")
                
        elif action == "reset":
            email = request.form.get("email")
            # TODO: Implement password reset functionality
            flash("Password reset link sent to your email (feature coming soon)", "info")
    
    return render_template("auth-html-page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Redirect to unified auth page"""
    if request.method == "POST":
        # Handle POST requests by forwarding to auth_page
        return auth_page()
    return redirect(url_for("auth_page"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Redirect to unified auth page"""
    if request.method == "POST":
        # Handle POST requests by forwarding to auth_page
        return auth_page()
    return redirect(url_for("auth_page"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form.get("email")
        # TODO: Implement password reset email functionality
        flash("If an account with that email exists, a password reset link has been sent.", "info")
        return redirect(url_for("login"))
    return render_template("auth-html-page.html")

@app.route("/reset_password_confirm", methods=["GET", "POST"])
def reset_password_confirm():
    if request.method == "POST":
        # TODO: Implement password reset confirmation
        flash("Password has been reset successfully.", "success")
        return redirect(url_for("login"))
    return render_template("auth-html-page.html")

@app.route("/update_profile", methods=["POST"])
def update_profile():
    if 'user_id' not in session:
        flash("Please log in to update your profile.", "warning")
        return redirect(url_for("login"))
    
    # TODO: Implement profile update functionality
    flash("Profile updated successfully!", "success")
    return redirect(url_for("profile_page"))

@app.route("/update_preferences", methods=["POST"])
def update_preferences():
    if 'user_id' not in session:
        flash("Please log in to update preferences.", "warning")
        return redirect(url_for("login"))
    
    # TODO: Implement preferences update functionality
    flash("Preferences updated successfully!", "success")
    return redirect(url_for("profile_page"))

@app.route("/change_password", methods=["POST"])
def change_password():
    if 'user_id' not in session:
        flash("Please log in to change password.", "warning")
        return redirect(url_for("login"))
    
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    
    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("profile_page"))
    
    # TODO: Implement password change functionality
    flash("Password changed successfully!", "success")
    return redirect(url_for("profile_page"))

# --- Template preview routes (development only) ---
# NOTE: Removed duplicate @app.route("/auth") to fix route conflict

@app.route("/profile")
def profile_page():
    if 'user_id' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))
    
    # Get user data from database
    user = auth_controller.get_user_by_id(session['user_id'])
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("login"))
    
    # Add default values for template compatibility
    user.update({
        'average_rating': user.get('average_rating', 0),
        'total_reviews': user.get('total_reviews', 0),
        'verification_status': user.get('verification_status', 'pending'),
        'joined_date': '2024-01-01'  # TODO: Use actual created_at date
    })
    
    return render_template("profile-html-page.html", user=user)

@app.route("/browse")
def browse_page():
    if 'user_id' not in session:
        flash("Please log in to browse profiles.", "warning")
        return redirect(url_for("login"))
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Get escort profiles from database
    escort_repo = EscortRepository(db)
    profiles = escort_repo.get_escort_profiles(limit=per_page, offset=offset)
    total_profiles = escort_repo.get_total_escort_count()
    total_pages = (total_profiles + per_page - 1) // per_page
    
    return render_template("browse-html-page.html", 
                         profiles=profiles,
                         current_page=page,
                         total_pages=total_pages,
                         total_profiles=total_profiles)

@app.route("/booking")
def booking_page():
    if 'user_id' not in session:
        flash("Please log in to make bookings.", "warning")
        return redirect(url_for("login"))
    
    # Mock data for booking page
    bookings = []  # TODO: Fetch from database
    return render_template("booking-html-page.html", bookings=bookings)

@app.route("/payment")
def payment_page():
    if 'user_id' not in session:
        flash("Please log in to view payments.", "warning")
        return redirect(url_for("login"))
    
    # Get user data from database
    user = auth_controller.get_user_by_id(session['user_id'])
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("login"))
    
    # Mock data for payment page
    payments = []  # TODO: Fetch from database
    return render_template("payment-html-page.html", payments=payments, user=user)

@app.route("/messaging")
def messaging_page():
    if 'user_id' not in session:
        flash("Please log in to view messages.", "warning")
        return redirect(url_for("login"))
    
    # Mock data for messaging page
    conversations = []  # TODO: Fetch from database
    return render_template("messaging-html-page.html", conversations=conversations)

@app.route("/dashboard")
def dashboard_page():
    if 'user_id' not in session:
        flash("Please log in to view your dashboard.", "warning")
        return redirect(url_for("login"))
    
    # Get user data from database
    user = auth_controller.get_user_by_id(session['user_id'])
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("login"))
    
    # Get user statistics from database
    stats = auth_controller.get_user_stats(session['user_id'])
    
    # Add default values for template compatibility
    user.update({
        'average_rating': user.get('average_rating', 0),
        'total_reviews': user.get('total_reviews', 0)
    })
    
    # Mock chart data for dashboard (TODO: implement real chart data)
    earnings_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    earnings_data = [200, 300, 250, 400, 350, 500]
    bookings_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    bookings_data = [1, 2, 0, 3, 1, 2, 1]
    growth_labels = ['Q1', 'Q2', 'Q3', 'Q4']
    growth_data = [10, 25, 15, 30]
    seekers_data = [30, 45, 25]  # Sample data for seekers chart
    escorts_data = [20, 35, 40]  # Sample data for escorts chart
    
    return render_template("dashboard-html-page.html", 
                         user=user, 
                         stats=stats,
                         earnings_labels=earnings_labels,
                         earnings_data=earnings_data,
                         bookings_labels=bookings_labels,
                         bookings_data=bookings_data,
                         growth_labels=growth_labels,
                         growth_data=growth_data,
                         seekers_data=seekers_data,
                         escorts_data=escorts_data)

@app.route("/admin")
def admin_page():
    if 'user_id' not in session:
        flash("Please log in to access admin panel.", "warning")
        return redirect(url_for("login"))
    
    if session.get('user_role') != 'admin':
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("dashboard_page"))
    
    # Mock admin data
    admin_stats = {
        'total_users': 0,
        'total_escorts': 0,
        'total_seekers': 0,
        'total_bookings': 0,
        'pending_verifications': 0
    }
    
    return render_template("admin-html-page.html", stats=admin_stats)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=(os.environ.get("FLASK_ENV") == "development")
    )