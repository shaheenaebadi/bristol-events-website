# =============================================
# BRISTOL EVENTS - FLASK APPLICATION
# Student ID: [Your Student ID]
# Main Application File with Routing & Logic
# =============================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import re

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Change if you have a password
app.config['MYSQL_DB'] = 'bristol_events'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# =============================================
# HELPER FUNCTIONS
# =============================================

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def calculate_discount(event_date_str, is_student=False):
    """Calculate discount based on advance booking and student status"""
    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
        today = datetime.now()
        days_until_event = (event_date - today).days
        
        discount = 0
        
        # Early bird discount
        if 50 <= days_until_event <= 60:
            discount = 20
        elif 35 <= days_until_event < 50:
            discount = 15
        elif 25 <= days_until_event < 35:
            discount = 10
        elif 15 <= days_until_event < 25:
            discount = 5
        
        # Add student discount (10%)
        if is_student:
            # Combine discounts
            discount = min(discount + 10, 30)  # Max 30% total discount
        
        return discount
    except:
        return 0

def calculate_final_amount(ticket_price, num_tickets, discount_percentage):
    """Calculate final amount after discount"""
    total = float(ticket_price) * int(num_tickets)
    discount_amount = total * (float(discount_percentage) / 100)
    final_amount = total - discount_amount
    return round(final_amount, 2)

def get_tickets_remaining(event_id):
    """Get number of tickets remaining for an event"""
    cur = mysql.connection.cursor()
    
    # Get venue capacity
    cur.execute('''
        SELECT v.capacity 
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        WHERE e.event_id = %s
    ''', (event_id,))
    result = cur.fetchone()
    capacity = result['capacity'] if result else 0
    
    # Get tickets already booked
    cur.execute('''
        SELECT COALESCE(SUM(number_of_tickets), 0) as tickets_booked
        FROM BOOKING
        WHERE event_id = %s AND booking_status = 'confirmed'
    ''', (event_id,))
    result = cur.fetchone()
    tickets_booked = result['tickets_booked'] if result else 0
    
    cur.close()
    
    return capacity - tickets_booked

# =============================================
# ROUTES - PUBLIC PAGES
# =============================================

@app.route('/')
def index():
    """Homepage with featured events"""
    cur = mysql.connection.cursor()
    
    # Get upcoming events (next 3)
    cur.execute('''
        SELECT e.*, v.venue_name, v.address, ec.category_name
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
        WHERE e.start_date >= CURDATE()
        ORDER BY e.start_date
        LIMIT 3
    ''')
    featured_events = cur.fetchall()
    
    # Calculate remaining tickets for each event
    for event in featured_events:
        event['tickets_remaining'] = get_tickets_remaining(event['event_id'])
    
    cur.close()
    
    return render_template('index.html', events=featured_events)

@app.route('/events')
def events():
    """Browse all events with filtering"""
    cur = mysql.connection.cursor()
    
    # Get filter parameters
    category = request.args.get('category', '')
    venue = request.args.get('venue', '')
    search = request.args.get('search', '')
    free_only = request.args.get('free_only', '')
    
    # Build query
    query = '''
        SELECT e.*, v.venue_name, v.address, ec.category_name
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
        WHERE e.start_date >= CURDATE()
    '''
    params = []
    
    if category:
        query += ' AND ec.category_id = %s'
        params.append(category)
    
    if venue:
        query += ' AND v.venue_id = %s'
        params.append(venue)
    
    if search:
        query += ' AND (e.event_name LIKE %s OR e.event_description LIKE %s)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param])
    
    if free_only:
        query += ' AND e.ticket_price = 0'
    
    query += ' ORDER BY e.start_date'
    
    cur.execute(query, params)
    all_events = cur.fetchall()
    
    # Get categories for filter
    cur.execute('SELECT * FROM EVENT_CATEGORY')
    categories = cur.fetchall()
    
    # Get venues for filter
    cur.execute('SELECT * FROM VENUE')
    venues = cur.fetchall()
    
    # Calculate remaining tickets
    for event in all_events:
        event['tickets_remaining'] = get_tickets_remaining(event['event_id'])
    
    cur.close()
    
    return render_template('events.html', 
                         events=all_events, 
                         categories=categories, 
                         venues=venues)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Show event details"""
    cur = mysql.connection.cursor()
    
    # Get event details
    cur.execute('''
        SELECT e.*, v.venue_name, v.address, v.capacity, ec.category_name
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
        WHERE e.event_id = %s
    ''', (event_id,))
    event = cur.fetchone()
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events'))
    
    # Calculate remaining tickets
    event['tickets_remaining'] = get_tickets_remaining(event_id)
    
    # Get similar events (same category, different event)
    cur.execute('''
        SELECT e.*, v.venue_name, ec.category_name
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
        WHERE e.category_id = %s AND e.event_id != %s AND e.start_date >= CURDATE()
        LIMIT 3
    ''', (event['category_id'], event_id))
    similar_events = cur.fetchall()
    
    cur.close()
    
    return render_template('event_detail.html', event=event, similar_events=similar_events)

# =============================================
# ROUTES - BOOKING SYSTEM
# =============================================

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    """Book tickets for an event"""
    cur = mysql.connection.cursor()
    
    # Get event details
    cur.execute('''
        SELECT e.*, v.venue_name, v.capacity
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        WHERE e.event_id = %s
    ''', (event_id,))
    event = cur.fetchone()
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events'))
    
    # Check tickets remaining
    tickets_remaining = get_tickets_remaining(event_id)
    
    if request.method == 'POST':
        num_tickets = int(request.form.get('num_tickets', 1))
        
        # Validate number of tickets
        if num_tickets < 1:
            flash('Please select at least 1 ticket', 'error')
        elif num_tickets > tickets_remaining:
            flash(f'Only {tickets_remaining} tickets available', 'error')
        else:
            # Get user details
            cur.execute('SELECT is_student FROM USER WHERE user_id = %s', (session['user_id'],))
            user = cur.fetchone()
            is_student = user['is_student']
            
            # Calculate discount
            discount = calculate_discount(str(event['start_date']), is_student)
            
            # Calculate final amount
            final_amount = calculate_final_amount(event['ticket_price'], num_tickets, discount)
            
            # Create booking
            cur.execute('''
                INSERT INTO BOOKING 
                (user_id, event_id, booking_date, number_of_tickets, 
                 discount_percentage, student_discount_applied, final_amount, booking_status)
                VALUES (%s, %s, CURDATE(), %s, %s, %s, %s, 'confirmed')
            ''', (session['user_id'], event_id, num_tickets, discount, is_student, final_amount))
            
            booking_id = cur.lastrowid
            
            # Generate tickets
            for i in range(num_tickets):
                ticket_number = f"BCE-{event_id:04d}-{booking_id:04d}-{i+1:03d}"
                cur.execute('''
                    INSERT INTO TICKET (booking_id, ticket_number)
                    VALUES (%s, %s)
                ''', (booking_id, ticket_number))
            
            # Create payment record
            cur.execute('''
                INSERT INTO PAYMENT 
                (booking_id, payment_method, payment_amount, payment_status, transaction_id)
                VALUES (%s, 'Credit Card', %s, 'completed', %s)
            ''', (booking_id, final_amount, f'TXN-{booking_id:08d}'))
            
            mysql.connection.commit()
            
            flash(f'Booking confirmed! {num_tickets} tickets booked successfully.', 'success')
            return redirect(url_for('my_bookings'))
    
    cur.close()
    
    # Calculate preview discount
    cur.execute('SELECT is_student FROM USER WHERE user_id = %s', (session['user_id'],))
    user = cur.fetchone()
    is_student = user['is_student'] if user else False
    
    preview_discount = calculate_discount(str(event['start_date']), is_student)
    
    return render_template('booking.html', 
                         event=event, 
                         tickets_remaining=tickets_remaining,
                         preview_discount=preview_discount,
                         is_student=is_student)

@app.route('/my-bookings')
@login_required
def my_bookings():
    """Show user's bookings"""
    cur = mysql.connection.cursor()
    
    cur.execute('''
        SELECT b.*, e.event_name, e.start_date, e.end_date, v.venue_name
        FROM BOOKING b
        JOIN EVENT e ON b.event_id = e.event_id
        JOIN VENUE v ON e.venue_id = v.venue_id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
    ''', (session['user_id'],))
    bookings = cur.fetchall()
    
    # Get tickets for each booking
    for booking in bookings:
        cur.execute('SELECT * FROM TICKET WHERE booking_id = %s', (booking['booking_id'],))
        booking['tickets'] = cur.fetchall()
    
    cur.close()
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    cur = mysql.connection.cursor()
    
    # Get booking details
    cur.execute('''
        SELECT b.*, e.start_date
        FROM BOOKING b
        JOIN EVENT e ON b.event_id = e.event_id
        WHERE b.booking_id = %s AND b.user_id = %s
    ''', (booking_id, session['user_id']))
    booking = cur.fetchone()
    
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('my_bookings'))
    
    if booking['booking_status'] == 'cancelled':
        flash('Booking already cancelled', 'error')
        return redirect(url_for('my_bookings'))
    
    # Calculate cancellation fee
    event_date = booking['start_date']
    days_until_event = (event_date - datetime.now().date()).days
    
    cancellation_fee = 0
    if days_until_event < 25:
        cancellation_fee = booking['final_amount']  # 100%
    elif 25 <= days_until_event < 40:
        cancellation_fee = booking['final_amount'] * 0.4  # 40%
    
    # Update booking
    cur.execute('''
        UPDATE BOOKING
        SET booking_status = 'cancelled', cancellation_fee = %s
        WHERE booking_id = %s
    ''', (cancellation_fee, booking_id))
    
    mysql.connection.commit()
    cur.close()
    
    if cancellation_fee > 0:
        flash(f'Booking cancelled. Cancellation fee: £{cancellation_fee:.2f}', 'info')
    else:
        flash('Booking cancelled successfully. No cancellation fee.', 'success')
    
    return redirect(url_for('my_bookings'))

# =============================================
# ROUTES - AUTHENTICATION
# =============================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_student = 'is_student' in request.form
        
        # Validation
        errors = []
        
        if not all([first_name, last_name, email, password, confirm_password]):
            errors.append('All fields are required')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters')
        
        # Email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            errors.append('Invalid email format')
        
        # Check if email already exists
        cur = mysql.connection.cursor()
        cur.execute('SELECT user_id FROM USER WHERE email = %s', (email,))
        if cur.fetchone():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # Hash password
            password_hash = generate_password_hash(password)
            
            # Insert user
            cur.execute('''
                INSERT INTO USER 
                (first_name, last_name, email, password_hash, phone_number, is_student, user_type)
                VALUES (%s, %s, %s, %s, %s, %s, 'standard')
            ''', (first_name, last_name, email, password_hash, phone, is_student))
            
            mysql.connection.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        cur.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM USER WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password_hash'], password):
            # Set session
            session['user_id'] = user['user_id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            session['user_type'] = user['user_type']
            session['is_student'] = user['is_student']
            
            flash(f'Welcome back, {user["first_name"]}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# =============================================
# ROUTES - ADMIN
# =============================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    cur = mysql.connection.cursor()
    
    # Get statistics
    cur.execute('SELECT COUNT(*) as total FROM EVENT WHERE start_date >= CURDATE()')
    upcoming_events = cur.fetchone()['total']
    
    cur.execute('SELECT COUNT(*) as total FROM USER WHERE user_type = "standard"')
    total_users = cur.fetchone()['total']
    
    cur.execute('SELECT COUNT(*) as total FROM BOOKING WHERE booking_status = "confirmed"')
    total_bookings = cur.fetchone()['total']
    
    cur.execute('SELECT COALESCE(SUM(final_amount), 0) as total FROM BOOKING WHERE booking_status = "confirmed"')
    total_revenue = cur.fetchone()['total']
    
    # Recent bookings
    cur.execute('''
        SELECT b.*, e.event_name, u.first_name, u.last_name
        FROM BOOKING b
        JOIN EVENT e ON b.event_id = e.event_id
        JOIN USER u ON b.user_id = u.user_id
        ORDER BY b.created_at DESC
        LIMIT 10
    ''')
    recent_bookings = cur.fetchall()
    
    cur.close()
    
    return render_template('admin/dashboard.html',
                         upcoming_events=upcoming_events,
                         total_users=total_users,
                         total_bookings=total_bookings,
                         total_revenue=total_revenue,
                         recent_bookings=recent_bookings)

# =============================================
# ROUTES - STATIC PAGES
# =============================================

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

# =============================================
# ERROR HANDLERS
# =============================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# =============================================
# RUN APPLICATION
# =============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
