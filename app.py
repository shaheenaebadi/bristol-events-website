# =============================================
# BRISTOL EVENTS - SIMPLE VERSION (NO DATABASE)
# For Testing Design & Responsiveness
# =============================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-for-testing'

# Sample data (instead of database)
SAMPLE_EVENTS = [
    {
        'event_id': 1,
        'event_name': 'Bristol Balloon Fiesta',
        'event_description': 'Europe\'s largest annual hot air balloon event with over 100 balloons',
        'start_date': datetime(2026, 8, 7),
        'end_date': datetime(2026, 8, 10),
        'ticket_price': 15.00,
        'is_multi_day': True,
        'venue_name': 'Ashton Court Estate',
        'address': 'Ashton Court, Long Ashton, Bristol BS41 9JN',
        'category_name': 'Community',
        'capacity': 500,
        'tickets_remaining': 234
    },
    {
        'event_id': 2,
        'event_name': 'Bristol Music Festival',
        'event_description': 'Live performances from local and international artists',
        'start_date': datetime(2026, 7, 15),
        'end_date': datetime(2026, 7, 15),
        'ticket_price': 25.00,
        'is_multi_day': False,
        'venue_name': 'Bristol Amphitheatre',
        'address': 'Harbourside, Bristol BS1 5DB',
        'category_name': 'Musical',
        'capacity': 300,
        'tickets_remaining': 87
    },
    {
        'event_id': 3,
        'event_name': 'Art Exhibition: Modern Bristol',
        'event_description': 'Contemporary art exhibition featuring local Bristol artists',
        'start_date': datetime(2026, 6, 20),
        'end_date': datetime(2026, 6, 20),
        'ticket_price': 0.00,
        'is_multi_day': False,
        'venue_name': 'Bristol Museum & Art Gallery',
        'address': 'Queens Road, Bristol BS8 1RL',
        'category_name': 'Exhibition',
        'capacity': 200,
        'tickets_remaining': 156
    }
]

SAMPLE_CATEGORIES = [
    {'category_id': 1, 'category_name': 'Exhibition'},
    {'category_id': 2, 'category_name': 'Musical'},
    {'category_id': 3, 'category_name': 'Sports'},
    {'category_id': 4, 'category_name': 'Theatre'},
    {'category_id': 5, 'category_name': 'Workshop'},
    {'category_id': 6, 'category_name': 'Community'}
]

SAMPLE_VENUES = [
    {'venue_id': 1, 'venue_name': 'Ashton Court Estate'},
    {'venue_id': 2, 'venue_name': 'Bristol Amphitheatre'},
    {'venue_id': 3, 'venue_name': 'Bristol Museum & Art Gallery'}
]

# Temporary storage for users and bookings
USERS = {}
BOOKINGS = []

@app.route('/')
def index():
    """Homepage with featured events"""
    return render_template('index.html', events=SAMPLE_EVENTS[:3])

@app.route('/events')
def events():
    """Browse all events"""
    return render_template('events.html', 
                         events=SAMPLE_EVENTS,
                         categories=SAMPLE_CATEGORIES,
                         venues=SAMPLE_VENUES)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Show event details"""
    event = next((e for e in SAMPLE_EVENTS if e['event_id'] == event_id), None)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events'))
    
    similar_events = [e for e in SAMPLE_EVENTS if e['event_id'] != event_id][:3]
    return render_template('event_detail.html', event=event, similar_events=similar_events)

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
def book_event(event_id):
    """Book tickets for an event"""
    if 'user_id' not in session:
        flash('Please login to book tickets', 'error')
        return redirect(url_for('login'))
    
    event = next((e for e in SAMPLE_EVENTS if e['event_id'] == event_id), None)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events'))
    
    if request.method == 'POST':
        num_tickets = int(request.form.get('num_tickets', 1))
        
        # Create booking
        booking = {
            'booking_id': len(BOOKINGS) + 1,
            'user_id': session['user_id'],
            'event_id': event_id,
            'num_tickets': num_tickets,
            'total_amount': event['ticket_price'] * num_tickets
        }
        BOOKINGS.append(booking)
        
        flash(f'Booking confirmed! {num_tickets} tickets booked successfully.', 'success')
        return redirect(url_for('my_bookings'))
    
    return render_template('booking.html', 
                         event=event,
                         tickets_remaining=event['tickets_remaining'],
                         preview_discount=10,
                         is_student=session.get('is_student', False))

@app.route('/my-bookings')
def my_bookings():
    """Show user's bookings"""
    if 'user_id' not in session:
        flash('Please login to view bookings', 'error')
        return redirect(url_for('login'))
    
    user_bookings = [b for b in BOOKINGS if b['user_id'] == session['user_id']]
    
    # Add event details to bookings
    for booking in user_bookings:
        event = next((e for e in SAMPLE_EVENTS if e['event_id'] == booking['event_id']), None)
        booking.update({
            'event_name': event['event_name'] if event else 'Unknown',
            'start_date': event['start_date'] if event else datetime.now(),
            'venue_name': event['venue_name'] if event else 'Unknown',
            'booking_status': 'confirmed',
            'final_amount': booking['total_amount']
        })
    
    return render_template('my_bookings.html', bookings=user_bookings)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        is_student = 'is_student' in request.form
        
        if email in USERS:
            flash('Email already registered', 'error')
        else:
            user_id = len(USERS) + 1
            USERS[email] = {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'password_hash': generate_password_hash(password),
                'is_student': is_student
            }
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = USERS.get(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            session['is_student'] = user['is_student']
            
            flash(f'Welcome back, {user["first_name"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
