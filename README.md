# BRISTOL EVENTS MANAGEMENT SYSTEM
### Student ID: [Your Student ID]
### Module: Web Development and Databases (UFCFES-30-1)
### Date: January 2026

---

## PROJECT OVERVIEW

This project is a responsive website for Bristol Community Events (BCE), an organization promoting tourism in Bristol through a unified event management system. The system allows users to browse events, book tickets, and manage their bookings, while administrators can manage events, venues, and generate reports.

---

## PROGRESS REVIEW SUBMISSIONS

### Week 8 - Review Point 1 (HTML/CSS - 10 marks)

**Deliverables:**
1. ✅ Responsive website structure with HTML5
2. ✅ Professional CSS styling with color contrast and legibility
3. ✅ Responsive design for 3 screen sizes (mobile, tablet, desktop)
4. ✅ Logical navigation flow with all pages linked
5. ✅ Validated HTML syntax

**Pages Included:**
- index.html (Homepage with hero section and featured events)
- events.html (Browse events with filtering)
- event-detail.html (Detailed event information)
- login.html (Login/Registration forms)
- about.html (About the organization)
- contact.html (Contact form and information)

**Responsive Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1023px
- Desktop: ≥ 1024px

**Key Features:**
- Mobile-first responsive design
- Gradient color schemes for visual appeal
- Clear typography and readability
- Intuitive navigation with hamburger menu on mobile
- Professional look and feel throughout

---

### Term 2 - Week 2 - Review Point (Database - 10 marks)

**Deliverables:**
1. ✅ Complete ERD showing all entities and relationships
2. ✅ Database in 3rd Normal Form (3NF)
3. ✅ Explanation of normalization with data examples
4. ✅ SQL script to create all tables with constraints
5. ✅ Sample data inserted into all tables

**Database Files:**
- `database/ERD_AND_NORMALIZATION.md` - Complete ERD and normalization documentation
- `database/bristol_events.sql` - SQL script with all table definitions and sample data

**Database Tables:**
1. USER - User accounts (standard and admin)
2. VENUE - Event venues with capacity
3. EVENT_CATEGORY - Event types
4. EVENT - Event information
5. BOOKING - Ticket bookings
6. TICKET - Individual tickets
7. WAITING_LIST - Waiting list for full events
8. PAYMENT - Payment records

**Normalization:**
- Detailed explanation of 1NF, 2NF, and 3NF
- Examples showing transformation at each level
- Final schema eliminates redundancy and transitive dependencies

---

## FILE STRUCTURE

```
bristol-events-website/
│
├── index.html                  # Homepage
├── events.html                 # Events listing page
├── event-detail.html          # Event details page
├── login.html                 # Login/Registration page
├── about.html                 # About us page
├── contact.html               # Contact page
│
├── css/
│   └── styles.css             # Main stylesheet (responsive)
│
├── js/
│   └── script.js              # JavaScript for interactivity
│
├── database/
│   ├── ERD_AND_NORMALIZATION.md  # Database design documentation
│   └── bristol_events.sql        # SQL database script
│
└── README.md                  # This file
```

---

## HOW TO RUN THE WEBSITE

### Option 1: Open Directly in Browser
1. Extract the ZIP file
2. Navigate to the project folder
3. Double-click `index.html` to open in your default browser
4. Navigate through the website using the menu

### Option 2: Using a Local Server (Recommended)
1. Install a local server (e.g., XAMPP, WAMP, or VS Code Live Server)
2. Place the project folder in the server's htdocs/www directory
3. Access via `http://localhost/bristol-events-website/`

### Testing Responsive Design:
1. Open the website in a browser
2. Press F12 to open Developer Tools
3. Click the device toolbar icon (or press Ctrl+Shift+M)
4. Test on different screen sizes:
   - Mobile: 375px (iPhone)
   - Tablet: 768px (iPad)
   - Desktop: 1024px+ (Desktop)

---

## HOW TO SET UP THE DATABASE

### Prerequisites:
- MySQL Server installed (XAMPP includes MySQL)
- phpMyAdmin or MySQL Workbench

### Setup Steps:

1. **Start MySQL Server**
   - If using XAMPP: Start Apache and MySQL from XAMPP Control Panel

2. **Import Database**
   - Open phpMyAdmin (http://localhost/phpmyadmin/)
   - Click "New" to create a database
   - Click "Import" tab
   - Choose `database/bristol_events.sql` file
   - Click "Go"

3. **Alternative: Command Line**
   ```bash
   mysql -u root -p < database/bristol_events.sql
   ```

4. **Verify Database**
   - Database name: `bristol_events`
   - 8 tables should be created
   - Sample data should be inserted

### Database Credentials:
- Database: `bristol_events`
- Default User: `root`
- Password: (leave empty for XAMPP default, or your MySQL password)

---

## FEATURES IMPLEMENTED

### Week 8 Requirements (HTML/CSS):

✅ **Web pages for all website information needs** (1.5 marks)
- Homepage with hero section
- Events browsing page with filters
- Event detail pages
- Login/Registration pages
- About us page
- Contact page with form

✅ **Creative use of HTML tags, logical flow, all pages linked** (2.5 marks)
- Semantic HTML5 elements (nav, section, footer)
- Logical page structure and flow
- All pages interconnected via navigation
- No broken links

✅ **Responsive on three screen sizes** (2.5 marks)
- Mobile (< 768px): Hamburger menu, single column layout
- Tablet (768-1023px): Two-column grids
- Desktop (≥ 1024px): Multi-column layouts, full navigation

✅ **Nice look & feel** (2.5 marks)
- Professional gradient color schemes
- High color contrast for readability
- Clear typography (Segoe UI font family)
- Proper spacing and visual hierarchy
- Card-based layouts for events
- Hover effects and transitions

✅ **Website syntax is validated** (1 mark)
- Valid HTML5 syntax
- Proper CSS formatting
- No console errors

---

### Term 2 Week 2 Requirements (Database):

✅ **ERD with all requirements** (3 marks)
- Complete Entity Relationship Diagram
- All entities identified (8 tables)
- Relationships clearly defined
- Attributes with data types
- Primary and Foreign keys marked
- Multiplicities shown

✅ **Database in 1NF with examples** (1 mark)
- No repeating groups
- Atomic values only
- Examples showing transformation from unnormalized to 1NF

✅ **Database in 2NF** (1 mark)
- No partial dependencies
- All non-key attributes depend on full primary key
- Examples provided

✅ **2NF transformation examples** (1 mark)
- Clear examples showing removal of partial dependencies
- Before and after tables

✅ **Database in 3NF** (1 mark)
- No transitive dependencies
- Non-key attributes depend only on primary key
- Proper normalization maintained

✅ **3NF transformation examples** (1 mark)
- Examples showing elimination of transitive dependencies
- Explanation of derived/calculated fields removal

✅ **Error-free SQL with referential integrity** (2 marks)
- Complete SQL script creates database successfully
- All constraints properly applied (PK, FK, CHECK, UNIQUE)
- Referential integrity enforced
- Indexes for optimization
- Sample data inserted without errors
- Can be verified by creating database in MySQL

---

## DESIGN DECISIONS

### Color Scheme:
- Primary: Purple gradient (#667eea to #764ba2)
- Secondary: White with subtle grays
- Accent: Various gradients for event cards
- Background: Light gray (#f8f9fa)

### Typography:
- Font Family: Segoe UI (fallback to system fonts)
- Base Size: 16px
- Line Height: 1.6 for readability

### Layout:
- Mobile-first approach
- Maximum content width: 1200px
- Consistent spacing using padding and margins
- Grid and Flexbox for layouts

---

## BUSINESS LOGIC IMPLEMENTATION (For Future Development)

The database is designed to support the following business logic:

### Discount Calculations:
1. **Early Bird Discounts:**
   - 50-60 days in advance: 20% off
   - 35-50 days: 15% off
   - 25-35 days: 10% off
   - 15-25 days: 5% off

2. **Student Discount:**
   - 10% off on all events (requires student ID verification)

3. **Combined Discounts:**
   - Early bird + student discount can be applied together

### Cancellation Policy:
- 40+ days before: No cancellation fee
- 25-39 days: 40% cancellation fee
- Within 25 days: 100% cancellation fee (no refund)

### Capacity Management:
- Each venue has maximum capacity
- Bookings tracked to prevent overbooking
- Waiting list system for fully booked events

### Multi-Day Events:
- Events can span multiple days
- Price calculated as: total_price / days_count
- Users can book individual days or full event

---

## VALIDATION

### HTML Validation:
All HTML files follow HTML5 standards and can be validated at:
https://validator.w3.org/

### CSS Validation:
CSS file follows CSS3 standards and can be validated at:
https://jigsaw.w3.org/css-validator/

### Database Validation:
Run the provided SQL script to verify:
- All tables created successfully
- Sample data inserted without errors
- Relationships enforced through foreign keys
- Queries execute correctly

---

## TESTING CHECKLIST

### Website Testing:
- [ ] All pages load without errors
- [ ] Navigation works on all pages
- [ ] Responsive design works on mobile (375px)
- [ ] Responsive design works on tablet (768px)
- [ ] Responsive design works on desktop (1024px+)
- [ ] Mobile hamburger menu functions correctly
- [ ] All links are functional
- [ ] Forms display correctly
- [ ] CSS animations and transitions work

### Database Testing:
- [ ] Database creates successfully from SQL script
- [ ] All 8 tables are created
- [ ] Sample data is inserted
- [ ] Foreign key constraints work
- [ ] SELECT queries return expected results
- [ ] No orphaned records exist

---

## FUTURE ENHANCEMENTS (For Final Submission)

1. **Backend Integration:**
   - Python Flask for server-side processing
   - User authentication system
   - Dynamic data loading from database

2. **Booking System:**
   - Real-time ticket availability
   - Automatic discount calculation
   - Payment integration (simulated)
   - Booking confirmation emails

3. **Admin Dashboard:**
   - Event management (CRUD operations)
   - User management
   - Revenue reports
   - Booking analytics

4. **Security Features:**
   - Password hashing
   - SQL injection prevention
   - XSS protection
   - CSRF tokens

5. **Additional Features:**
   - Waiting list automation
   - Cancellation processing
   - Multi-day event booking
   - Advanced filtering and search

---

## CREDITS

**Student:** [Your Name]
**Student ID:** [Your Student ID]
**Module:** UFCFES-30-1 - Web Development and Databases
**Institution:** UWE Bristol
**Academic Year:** 2025-26

---

## CONTACT

For any questions or issues regarding this project:
- Email: [Your Email]
- Module Leader: Zaheer Khan and Barkha Javed

---

## LICENSE

This project is submitted as coursework for UFCFES-30-1 module at UWE Bristol. All rights reserved.

---

**Last Updated:** January 28, 2026
