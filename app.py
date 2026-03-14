# =============================================
# BRISTOL EVENTS - FLASK + MYSQL APPLICATION
# Phases 1, 2 & 3: DB events, auth, bookings
# =============================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import MySQLdb.cursors

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bristol-events-secret-key-2026'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bristol_events'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# ──────────────────────────────────────────
# Business Logic Helpers
# ──────────────────────────────────────────

def get_advance_discount(days_until_event):
    """Return advance-booking discount percentage based on days until event."""
    if days_until_event >= 50: return 20
    if days_until_event >= 35: return 15
    if days_until_event >= 25: return 10
    if days_until_event >= 15: return 5
    return 0


def get_cancellation_charge(days_until_event):
    """Return cancellation charge percentage based on days until event."""
    if days_until_event >= 40: return 0
    if days_until_event >= 25: return 40
    return 100  # within 25 days: full charge


def fix_seed_passwords():
    """Replace placeholder seed passwords with real werkzeug hashes (runs once)."""
    import MySQLdb
    seed = {
        'admin@bristolevents.com': 'Admin123!',
        'john.smith@email.com':    'Password1!',
        'emma.j@email.com':        'Password1!',
        'mike.w@email.com':        'Password1!',
        'sarah.b@email.com':       'Password1!',
        'david.jones@email.com':   'Password1!',
        'lisa.t@email.com':        'Password1!',
        'james.d@email.com':       'Password1!',
    }
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='',
                               db='bristol_events',
                               cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        for email, pw in seed.items():
            cur.execute("SELECT password_hash FROM USER WHERE email=%s", (email,))
            row = cur.fetchone()
            if row and not row['password_hash'].startswith('pbkdf2:'):
                cur.execute("UPDATE USER SET password_hash=%s WHERE email=%s",
                            (generate_password_hash(pw), email))
        conn.commit()
        cur.close()
        conn.close()
        print("Seed passwords set up.")
    except Exception as e:
        print(f"DB setup warning (MySQL may not be running): {e}")


# ──────────────────────────────────────────
# Shared DB Query
# ──────────────────────────────────────────

def query_events(extra_where='', params=(), limit=None):
    """
    Return events joined with venue + category + tickets_remaining.
    extra_where: additional WHERE conditions (without the WHERE keyword prefix,
                 appended with AND).
    """
    where = "WHERE e.start_date >= CURDATE()"
    if extra_where:
        where += f" AND ({extra_where})"

    limit_clause = f"LIMIT {int(limit)}" if limit else ""

    sql = f"""
        SELECT e.*,
               v.venue_name, v.address, v.capacity,
               ec.category_name,
               (v.capacity - COALESCE(
                   SUM(CASE WHEN b.booking_status='confirmed'
                            THEN b.number_of_tickets ELSE 0 END), 0)
               ) AS tickets_remaining
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
        LEFT JOIN BOOKING b ON e.event_id = b.event_id
        {where}
        GROUP BY e.event_id
        ORDER BY e.start_date ASC
        {limit_clause}
    """
    cur = mysql.connection.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_event_by_id(event_id):
    """Return a single event (no start_date >= CURDATE filter) by event_id."""
    sql = """
        SELECT e.*,
               v.venue_name, v.address, v.capacity,
               ec.category_name,
               (v.capacity - COALESCE(
                   SUM(CASE WHEN b.booking_status='confirmed'
                            THEN b.number_of_tickets ELSE 0 END), 0)
               ) AS tickets_remaining
        FROM EVENT e
        JOIN VENUE v ON e.venue_id = v.venue_id
        JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
        LEFT JOIN BOOKING b ON e.event_id = b.event_id
        WHERE e.event_id = %s
        GROUP BY e.event_id
    """
    cur = mysql.connection.cursor()
    cur.execute(sql, (event_id,))
    row = cur.fetchone()
    cur.close()
    return row


# ──────────────────────────────────────────
# Routes — Public Pages
# ──────────────────────────────────────────

@app.route('/')
def index():
    events = query_events(limit=3)
    return render_template('index.html', events=events)


@app.route('/events')
def events():
    category_filter = request.args.get('category', '').strip()
    free_only = request.args.get('free_only', '')

    extra_where_parts = []
    params = []

    if category_filter:
        try:
            cat_id = int(category_filter)
            extra_where_parts.append("ec.category_id = %s")
            params.append(cat_id)
        except ValueError:
            pass

    if free_only:
        extra_where_parts.append("e.ticket_price = 0")

    extra_where = " AND ".join(extra_where_parts)
    events_list = query_events(extra_where=extra_where, params=tuple(params))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EVENT_CATEGORY ORDER BY category_name")
    categories = cur.fetchall()
    cur.close()

    return render_template('events.html',
                           events=events_list,
                           categories=categories,
                           selected_category=category_filter,
                           free_only=free_only)


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events'))

    similar_events = query_events(
        extra_where="e.event_id != %s AND ec.category_id = %s",
        params=(event_id, event['category_id']),
        limit=3
    )
    return render_template('event_detail.html', event=event, similar_events=similar_events)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# ──────────────────────────────────────────
# Routes — Authentication
# ──────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        email      = request.form.get('email', '').strip().lower()
        password   = request.form.get('password', '')
        phone      = request.form.get('phone_number', '').strip()
        is_student = 'is_student' in request.form

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('register.html')

        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id FROM USER WHERE email=%s", (email,))
        if cur.fetchone():
            flash('Email already registered', 'error')
            cur.close()
            return render_template('register.html')

        cur.execute(
            """INSERT INTO USER (first_name, last_name, email, password_hash,
                                 phone_number, is_student)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (first_name, last_name, email, generate_password_hash(password),
             phone, is_student)
        )
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM USER WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id']   = user['user_id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            session['is_student'] = bool(user['is_student'])
            session['user_type']  = user['user_type']

            flash(f"Welcome back, {user['first_name']}!", 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


# ──────────────────────────────────────────
# Routes — Booking System
# ──────────────────────────────────────────

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
def book_event(event_id):
    if 'user_id' not in session:
        flash('Please login to book tickets', 'error')
        return redirect(url_for('login', next=url_for('book_event', event_id=event_id)))

    event = get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events'))

    today             = date.today()
    days_until        = (event['start_date'] - today).days
    advance_discount  = get_advance_discount(days_until)
    student_discount  = 10 if session.get('is_student') else 0
    total_discount    = min(advance_discount + student_discount, 100)

    if request.method == 'POST':
        num_tickets = int(request.form.get('num_tickets', 1))

        # Booking deadline check
        if event['last_booking_date'] and today > event['last_booking_date']:
            flash('The booking deadline for this event has passed.', 'error')
            return redirect(url_for('event_detail', event_id=event_id))

        # 2-month advance limit
        if days_until > 60:
            flash('Bookings open 2 months before the event. Please check back later.', 'info')
            return redirect(url_for('event_detail', event_id=event_id))

        tickets_remaining = int(event['tickets_remaining'])

        # Event full → waiting list
        if tickets_remaining <= 0:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT waiting_id FROM WAITING_LIST WHERE user_id=%s AND event_id=%s AND status='waiting'",
                (session['user_id'], event_id)
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO WAITING_LIST (user_id, event_id) VALUES (%s, %s)",
                    (session['user_id'], event_id)
                )
                mysql.connection.commit()
                flash('This event is full. You have been added to the waiting list!', 'info')
            else:
                flash('You are already on the waiting list for this event.', 'info')
            cur.close()
            return redirect(url_for('my_bookings'))

        # Not enough tickets
        if tickets_remaining < num_tickets:
            flash(f'Only {tickets_remaining} ticket(s) remaining. Please select fewer.', 'error')
            return redirect(url_for('book_event', event_id=event_id))

        # Calculate final amount
        base_price     = float(event['ticket_price'])
        subtotal       = base_price * num_tickets
        final_amount   = round(subtotal * (1 - total_discount / 100), 2)

        cur = mysql.connection.cursor()

        # Insert booking
        cur.execute(
            """INSERT INTO BOOKING
               (user_id, event_id, booking_date, number_of_tickets,
                discount_percentage, student_discount_applied, final_amount, booking_status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, 'confirmed')""",
            (session['user_id'], event_id, today, num_tickets,
             total_discount, bool(session.get('is_student')), final_amount)
        )
        booking_id = cur.lastrowid

        # Insert individual tickets
        for i in range(1, num_tickets + 1):
            ticket_num = f"BCE-{today.year}-{booking_id:04d}-{i:03d}"
            cur.execute(
                "INSERT INTO TICKET (booking_id, ticket_number) VALUES (%s, %s)",
                (booking_id, ticket_num)
            )

        mysql.connection.commit()
        cur.close()

        flash(f'Booking confirmed! {num_tickets} ticket(s) booked for {event["event_name"]}.', 'success')
        return redirect(url_for('my_bookings'))

    return render_template('booking.html',
                           event=event,
                           tickets_remaining=event['tickets_remaining'],
                           preview_discount=total_discount,
                           is_student=session.get('is_student', False))


@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please login to view your bookings', 'error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute(
        """SELECT b.*,
                  b.number_of_tickets AS num_tickets,
                  e.event_name, e.start_date,
                  v.venue_name
           FROM BOOKING b
           JOIN EVENT e ON b.event_id = e.event_id
           JOIN VENUE v ON e.venue_id = v.venue_id
           WHERE b.user_id = %s
           ORDER BY b.created_at DESC""",
        (session['user_id'],)
    )
    bookings = cur.fetchall()
    cur.close()

    return render_template('my_bookings.html', bookings=bookings)


@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute(
        """SELECT b.*, e.start_date, e.event_name
           FROM BOOKING b
           JOIN EVENT e ON b.event_id = e.event_id
           WHERE b.booking_id = %s AND b.user_id = %s AND b.booking_status = 'confirmed'""",
        (booking_id, session['user_id'])
    )
    booking = cur.fetchone()

    if not booking:
        flash('Booking not found or already cancelled.', 'error')
        cur.close()
        return redirect(url_for('my_bookings'))

    days_until       = (booking['start_date'] - date.today()).days
    charge_pct       = get_cancellation_charge(days_until)
    cancellation_fee = round(float(booking['final_amount']) * charge_pct / 100, 2)

    cur.execute(
        "UPDATE BOOKING SET booking_status='cancelled', cancellation_fee=%s WHERE booking_id=%s",
        (cancellation_fee, booking_id)
    )

    # Notify first person on waiting list
    cur.execute(
        """SELECT * FROM WAITING_LIST WHERE event_id=%s AND status='waiting'
           ORDER BY joined_at ASC LIMIT 1""",
        (booking['event_id'],)
    )
    next_in_line = cur.fetchone()
    if next_in_line:
        cur.execute(
            "UPDATE WAITING_LIST SET status='offered', notified=TRUE WHERE waiting_id=%s",
            (next_in_line['waiting_id'],)
        )

    mysql.connection.commit()
    cur.close()

    if charge_pct == 0:
        flash(f'Booking for "{booking["event_name"]}" cancelled. No fee applied.', 'success')
    else:
        flash(
            f'Booking for "{booking["event_name"]}" cancelled. '
            f'Cancellation fee: £{cancellation_fee:.2f} ({charge_pct}%).',
            'warning'
        )

    return redirect(url_for('my_bookings'))


# ──────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────

if __name__ == '__main__':
    fix_seed_passwords()
    app.run(debug=True, host='0.0.0.0', port=5000)
