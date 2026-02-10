# 🌸 BRISTOL EVENTS - COMPLETE IMPLEMENTATION GUIDE
## Girly Aesthetic Website with Flask Backend

**Student ID:** [Your Student ID]  
**Date:** January 2026

---

## 📋 TABLE OF CONTENTS

1. [Overview of Changes](#overview)
2. [What's New - All Features](#whats-new)
3. [Installation & Setup](#installation)
4. [File Structure](#file-structure)
5. [How to Run](#how-to-run)
6. [Features Explained](#features-explained)
7. [Testing Guide](#testing-guide)
8. [Marking Criteria Coverage](#marking-criteria)

---

## 🎯 OVERVIEW OF CHANGES

I've completely rebuilt your website with these major improvements:

### ✨ NEW DESIGN
- **Girly Aesthetic Theme**: Pink, purple, and lavender color scheme
- **Modern UI**: Rounded corners, gradients, soft shadows
- **Better Typography**: Poppins font for a more elegant look
- **Animations**: Smooth transitions and hover effects

### 🚀 NEW FEATURES
- **Flask Backend**: Full server-side processing
- **Database Integration**: MySQL with all tables working
- **Booking System**: Complete booking workflow
- **User Authentication**: Login/Register with password hashing
- **Dynamic Content**: All data loaded from database
- **Responsive Images**: Images scale with screen size
- **Discount Calculation**: Automatic early bird + student discounts
- **Security**: SQL injection prevention, XSS protection

---

## 🆕 WHAT'S NEW - ALL FEATURES

### 1. AESTHETIC GIRLY DESIGN ✨
- **Pink/Purple gradient** color scheme throughout
- **Soft shadows** and rounded edges
- **Emoji icons** for a fun, friendly feel
- **Hover animations** on cards and buttons
- **Beautiful gradients** on hero sections

### 2. HORIZONTAL NAVBAR 📱
- **Desktop**: Full menu always visible
- **Tablet**: Full menu visible
- **Mobile**: Hamburger menu that slides down
- **Active state**: Current page highlighted in pink
- **Smooth transitions**: Menu animations

### 3. BOOKING PAGE 🎟️
- **Step-by-step process**: Visual booking steps
- **Live price calculation**: Updates as you select tickets
- **Discount display**: Shows all applicable discounts
- **Event summary**: Clear overview of what you're booking
- **Form validation**: Prevents booking more than available tickets
- **Important info**: Cancellation policy clearly shown

### 4. CLICKABLE EVENT IMAGES 🖼️
- **Homepage events**: Click image to see details
- **Hover effect**: Image zooms and overlay appears
- **Book button**: Appears on hover
- **Category-specific images**: Different gradient for each type
- **Responsive**: Images scale from 200px (mobile) to 300px (desktop)

### 5. RESPONSIVE TEXT/IMAGES 📏
- **Mobile (< 768px)**:
  - Base font: 14px
  - Images: 200px height
  - Single column layouts
  
- **Tablet (768-1023px)**:
  - Base font: 17px
  - Images: 280px height
  - Two column layouts
  
- **Desktop (≥ 1024px)**:
  - Base font: 18px
  - Images: 300px height
  - Three/Four column layouts

### 6. WORKING DATABASE (SQL) 💾
- **All 8 tables** created and working
- **Sample data** inserted
- **Foreign keys** enforcing referential integrity
- **Queries** optimized with indexes
- **Transactions** for data consistency

### 7. FLASK BACKEND 🔧
- **User authentication**: Registration, login, logout
- **Session management**: Tracks logged-in users
- **Password hashing**: Secure password storage
- **Booking logic**: Handles all booking calculations
- **Discount calculation**: Automatic based on date and user type
- **Input validation**: Prevents invalid data
- **SQL injection prevention**: Parameterized queries
- **Error handling**: Graceful error messages

---

## 💻 INSTALLATION & SETUP

### Prerequisites:
1. **Python 3.8+** installed
2. **MySQL Server** installed (via XAMPP or standalone)
3. **pip** (Python package manager)

### Step 1: Install Required Python Packages

Create a file called `requirements.txt`:

```
Flask==2.3.2
Flask-MySQLdb==1.0.1
Werkzeug==2.3.6
mysqlclient==2.2.0
```

Then install:
```bash
pip install -r requirements.txt
```

**Note:** On Windows, if `mysqlclient` fails, install it from here:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Step 2: Setup MySQL Database

1. **Start MySQL** (via XAMPP or command line)
2. **Open phpMyAdmin** or MySQL Workbench
3. **Import the database**:
   - Click "Import"
   - Select `bristol_events.sql`
   - Click "Go"

**OR via command line:**
```bash
mysql -u root -p < database/bristol_events.sql
```

### Step 3: Configure Database Connection

Edit `app.py` lines 14-17:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password (if any)
app.config['MYSQL_DB'] = 'bristol_events'
```

### Step 4: Add Sample Event Images (Optional)

Create these folders:
```
bristol-events-flask/static/images/
```

Add images named:
- `exhibition.jpg`
- `music.jpg`
- `sports.jpg`
- `theatre.jpg`
- `workshop.jpg`
- `community.jpg`

**Note:** If images are missing, the site will show gradient backgrounds instead (still looks great!).

---

## 📁 FILE STRUCTURE

```
bristol-events-flask/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
│
├── static/                         # Static files (CSS, JS, Images)
│   ├── css/
│   │   └── styles.css             # Main stylesheet (girly design)
│   ├── js/
│   │   └── script.js              # JavaScript for interactivity
│   └── images/                    # Event images
│       ├── exhibition.jpg
│       ├── music.jpg
│       ├── sports.jpg
│       ├── theatre.jpg
│       ├── workshop.jpg
│       └── community.jpg
│
├── templates/                      # HTML templates
│   ├── index.html                 # Homepage
│   ├── events.html                # Events listing
│   ├── event_detail.html          # Event details
│   ├── booking.html               # Booking page
│   ├── my_bookings.html           # User's bookings
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── about.html                 # About page
│   ├── contact.html               # Contact page
│   └── admin/
│       └── dashboard.html         # Admin dashboard
│
└── database/
    ├── bristol_events.sql         # Database schema + data
    └── ERD_AND_NORMALIZATION.md   # Database documentation
```

---

## 🚀 HOW TO RUN

### Option 1: Command Line

1. Open terminal/command prompt
2. Navigate to project folder:
   ```bash
   cd path/to/bristol-events-flask
   ```
3. Run Flask:
   ```bash
   python app.py
   ```
4. Open browser to: `http://localhost:5000`

### Option 2: VS Code

1. Open project in VS Code
2. Open `app.py`
3. Click "Run" button (or press F5)
4. Select "Flask" if prompted
5. Browser will open automatically

### Option 3: PyCharm

1. Open project in PyCharm
2. Right-click `app.py`
3. Select "Run 'app'"
4. Browser will open automatically

---

## ✨ FEATURES EXPLAINED

### 1. Homepage with Clickable Images

**How it works:**
- Events loaded from database
- Each event card is clickable
- On hover: Image zooms + overlay appears with "Book Now" button
- Images change based on event category
- If no image available, shows gradient background

**Code Location:**
- Template: `templates/index.html`
- CSS: Line 300-380 in `styles.css`
- Flask route: `@app.route('/')` in `app.py`

### 2. Booking System

**Complete workflow:**
1. User clicks "Book Now" on event
2. If not logged in → redirected to login
3. Booking page shows:
   - Event details
   - Ticket selector
   - Automatic discount calculation
   - Live price updates
4. User submits → booking created
5. Tickets generated automatically
6. Payment record created
7. Confirmation message shown

**Discount Logic:**
```python
# Early bird discounts
50-60 days in advance: 20% off
35-50 days: 15% off
25-35 days: 10% off
15-25 days: 5% off

# Student discount
Always: 10% off

# Combined (max 30%)
```

**Code Location:**
- Template: `templates/booking.html`
- Flask route: `@app.route('/book/<int:event_id>')` in `app.py`
- Discount calculation: Lines 46-66 in `app.py`

### 3. User Authentication

**Features:**
- **Registration**: Email, password, student status
- **Login**: Email + password
- **Session**: Maintains login state
- **Logout**: Clears session
- **Password Security**: Hashed with Werkzeug

**Test Users (from database):**
```
Admin:
Email: admin@bristolevents.com
Password: admin123 (after you set it up)

Standard User:
Email: john.smith@email.com
Password: password123 (after you set it up)
```

### 4. Responsive Design

**Breakpoints:**
```css
Mobile: max-width 767px
  - 1 column layouts
  - Hamburger menu
  - Font: 14px
  - Images: 200px

Tablet: 768px - 1023px
  - 2 column layouts
  - Full menu
  - Font: 17px
  - Images: 280px

Desktop: 1024px+
  - 3-4 column layouts
  - Full menu
  - Font: 18px
  - Images: 300px
```

### 5. Database Integration

**All tables working:**
1. USER - Stores user accounts
2. VENUE - Event venues
3. EVENT_CATEGORY - Event types
4. EVENT - All events
5. BOOKING - Ticket bookings
6. TICKET - Individual tickets
7. WAITING_LIST - For full events
8. PAYMENT - Payment records

**Sample queries in app:**
- Get upcoming events
- Filter by category/venue
- Calculate tickets remaining
- Get user's bookings
- Admin reports

---

## 🧪 TESTING GUIDE

### Test 1: Responsive Design
1. Open homepage
2. Press F12 (DevTools)
3. Press Ctrl+Shift+M (Device toolbar)
4. Test: 375px, 768px, 1440px
5. Check:
   - ✅ Hamburger menu on mobile
   - ✅ Images scale
   - ✅ Text size changes
   - ✅ Layouts change (1, 2, 3 columns)

### Test 2: Registration & Login
1. Go to Login/Register page
2. Click "Register here"
3. Fill form (check "I am a student")
4. Submit
5. Login with credentials
6. Should see "Welcome back!"

### Test 3: Booking System
1. Login as student
2. Go to homepage
3. Click on an event image
4. Click "Book Now"
5. Select number of tickets
6. Check discount is shown (10% student + early bird if applicable)
7. Check total updates when changing tickets
8. Submit booking
9. Should see confirmation

### Test 4: My Bookings
1. After booking, click "My Bookings"
2. Should see all your bookings
3. Should show:
   - Event name
   - Date
   - Number of tickets
   - Total amount
   - Ticket numbers

### Test 5: Database Verification
1. Open phpMyAdmin
2. Select `bristol_events` database
3. Click "Browse" on BOOKING table
4. Should see your booking
5. Check TICKET table - should have your tickets
6. Check PAYMENT table - should have payment record

---

## ✅ MARKING CRITERIA COVERAGE

### Element 1 (15 marks): Responsive Design
- ✅ **3 screen sizes**: Mobile, Tablet, Desktop
- ✅ **Images scale**: 200px → 280px → 300px
- ✅ **Text scales**: 14px → 17px → 18px
- ✅ **Layouts change**: 1 → 2 → 3 columns
- ✅ **Mobile menu**: Hamburger functionality

### Element 2 (15 marks): Database Design
- ✅ **ERD**: Complete with 8 tables
- ✅ **3NF**: Full normalization with examples
- ✅ **SQL**: Error-free with constraints
- ✅ **Sample data**: All tables populated

### Element 3 (30 marks): Business Logic
- ✅ **Flask**: Full server-side implementation
- ✅ **User system**: Register, login, logout
- ✅ **Booking logic**: Complete workflow
- ✅ **Dynamic pages**: Data from database
- ✅ **Discount calculation**: Early bird + student
- ✅ **Security**: Password hashing, SQL injection prevention
- ✅ **Error handling**: Validation and error messages

### Element 4 (20 marks): Presentation
- ✅ **Functional**: All features work
- ✅ **LESP covered**: Privacy, security implemented
- ✅ **Demo-ready**: Can show all features
- ✅ **Professional**: Girly aesthetic, clean code

---

## 🎨 CUSTOMIZATION TIPS

### Change Colors:
Edit `styles.css` lines 11-21:
```css
:root {
    --primary-pink: #ff6b9d;      /* Main pink */
    --primary-purple: #c44569;    /* Main purple */
    --light-pink: #ffeef4;        /* Light background */
    ...
}
```

### Add More Events:
1. Open phpMyAdmin
2. Go to EVENT table
3. Click "Insert"
4. Fill in details
5. Submit

### Change Secret Key (IMPORTANT for production):
Edit `app.py` line 13:
```python
app.config['SECRET_KEY'] = 'your-unique-secret-key-here'
```

---

## 🆘 TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install flask flask-mysqldb
```

### Issue: "Can't connect to MySQL server"
**Solution:**
1. Make sure MySQL is running (start in XAMPP)
2. Check username/password in `app.py`

### Issue: "Access denied for user"
**Solution:**
Change MySQL credentials in `app.py` lines 14-16

### Issue: "Template not found"
**Solution:**
Make sure `templates/` folder is in the same directory as `app.py`

### Issue: Images not showing
**Solution:**
Either add images to `static/images/` OR leave empty - gradients will show

---

## 📝 FINAL CHECKLIST

Before submitting:
- [ ] All Python packages installed
- [ ] Database imported successfully
- [ ] Flask app runs without errors
- [ ] Can register and login
- [ ] Can book an event
- [ ] Responsive design works on 3 sizes
- [ ] All links work
- [ ] Code is commented
- [ ] Student ID added to files

---

## 🎓 DEMO SCRIPT FOR TUTOR

**1. Show Responsive Design (2 min)**
- Open homepage
- F12 → Device toolbar
- Show 375px, 768px, 1440px
- Point out image/text scaling

**2. Show Booking System (3 min)**
- Register as student
- Click event image
- Show booking page
- Point out discount calculation
- Complete booking

**3. Show Database (2 min)**
- Open phpMyAdmin
- Show tables
- Show your booking in BOOKING table
- Show generated tickets in TICKET table

**4. Show Code (3 min)**
- Show `app.py` - Flask routing
- Show `styles.css` - responsive breakpoints
- Show `booking.html` - booking form

---

**Ready to submit! Good luck! 🌸✨**
