# Bristol Events Website — Refactoring Plan

## Context
The app currently has a working Flask skeleton (routes, Jinja2 templates, CSS, JS) but uses hardcoded Python dicts/lists instead of MySQL. The course requires: (1) a MySQL database in 3NF, (2) all data loaded dynamically from the DB via Flask/Jinja2, (3) a complete user system with standard + admin roles, and (4) full business logic (discounts, cancellation charges, waiting list, admin reports). A `bristol_events.sql` schema already exists and is well-designed (3NF, 7 tables) — the primary work is wiring Flask to MySQL and building out missing features.

**Deadlines:**
- PR3 Week 21: 24 March 2026 — pages + CSS load through Flask; one DB→template dynamic example
- PR3 Week 22: 31 March 2026 — form → Flask → DB → response working
- Final: 23 April 2026

---

## ✅ Session Log — 14 March 2026

### Completed This Session: Phases 1 + 2 + 3

**Phase 1 — MySQL Connection & Core Data Layer: DONE**
- `app.py` fully rewritten with `Flask-MySQLdb` (DictCursor)
- All hardcoded `SAMPLE_EVENTS`, `SAMPLE_CATEGORIES`, `SAMPLE_VENUES`, `USERS {}`, `BOOKINGS []` removed
- `query_events()` helper and `get_event_by_id()` helper added — handle JOIN with VENUE + EVENT_CATEGORY + tickets_remaining calculation
- Routes `/`, `/events`, `/event/<id>` all query live MySQL data
- `templates/events.html` updated with category dropdown + free-events checkbox filter form
- Verified: 4 upcoming events load correctly from DB

**Phase 2 — User Authentication via DB: DONE**
- `/register` POST inserts into `USER` table with `generate_password_hash`
- `/login` POST queries `USER WHERE email=%s`, uses `check_password_hash`
- Session now stores `user_id`, `user_name`, `is_student`, `user_type` (needed for admin check)
- `fix_seed_passwords()` function runs at startup (`if __name__ == '__main__'`) — replaces fake seed hashes with real werkzeug hashes
- Seed credentials: admin `admin@bristolevents.com` / `Admin123!` ; all others: `Password1!`

**Phase 3 — Booking System via DB: DONE**
- `/book/<id>` GET: calculates advance discount + student discount, passes to template
- `/book/<id>` POST: validates deadline, 60-day advance limit, ticket availability; INSERTs BOOKING + individual TICKETs; handles full-event → waiting list redirect
- `/my-bookings`: queries BOOKING JOIN EVENT JOIN VENUE for current user
- `/cancel-booking/<id>` POST: calculates cancellation fee, UPDATEs BOOKING, notifies first waiting list entry
- `templates/my_bookings.html`: updated column reference (`num_tickets`), added colour-coded status, added Cancel button with confirmation dialog

**Infrastructure**
- `Flask-MySQLdb==2.0.0` and `mysqlclient==2.2.8` installed
- All 9 DB tables verified (incl. `BOOKING_DAY` added by user)
- Flask app starts cleanly, DB connection confirmed

---

## ✅ Session Log — 14 March 2026 (Second session)

### Completed This Session: Phase 4 — Admin Panel: DONE

**Routes added to `app.py` (all protected with `admin_required()` helper):**
- `GET /admin` → `admin_dashboard` — stat cards: upcoming events, confirmed bookings, revenue, users
- `GET /admin/events` → `admin_events` — table of all events (incl. past) with edit/delete; passes `today=date.today()` for upcoming/past badge
- `GET/POST /admin/events/add` → `admin_add_event` — insert new event; handles multi-day fields
- `GET/POST /admin/events/edit/<id>` → `admin_edit_event` — pre-fills form; UPDATEs on POST
- `POST /admin/events/delete/<id>` → `admin_delete_event` — DELETEs event with JS confirm
- `GET/POST /admin/venues` → `admin_venues` — lists all venues + inline add-venue form
- `GET /admin/bookings` → `admin_bookings` — all bookings with user details; filter by `?status=confirmed/cancelled/pending`
- `GET /admin/reports` → `admin_reports` — 3 reports on one page (see below)

**`admin_required()` helper function added** — calls `abort(403)` if `session.get('user_type') != 'admin'`

**Templates created in `templates/admin/`:**
- `dashboard.html` — 4 stat cards (events, bookings, revenue, users) + quick-action buttons
- `events.html` — full table with upcoming/past badge, colour-coded tickets-remaining, Edit + Delete buttons
- `event_form.html` — shared Add/Edit form; multi-day fields toggle via JS; venue/category dropdowns from DB
- `venues.html` — add-venue form (inline, POST to same route) + venues table
- `bookings.html` — full bookings table with status filter tabs; shows customer, event, venue, discount, amount
- `reports.html` — 3 report tables:
  1. Revenue & Bookings Per Event (with running total in tfoot)
  2. Ticket Availability for upcoming events (fill-rate bar chart)
  3. Waiting List Summary per event

**Admin nav link** added to `index.html` and `events.html` navbars — visible only when `session.user_type == 'admin'`

**Admin sub-nav bar** (purple strip under main navbar) links between all 5 admin pages; active link is bold white.

**How to access admin:**
1. Login as `admin@bristolevents.com` / `Admin123!`
2. Click "Admin Panel" in the navbar, or go directly to `/admin`

---

## ✅ Session Log — 14 March 2026 (Bug fixes)

### Bug 1 — `booking.html` truncated (500 on `/book/<id>`): FIXED
- File was cut off mid-line at `const maxTickets = {{ ticket`
- Completed to `const maxTickets = {{ tickets_remaining }};` and added closing `</script></body></html>`

### Bug 2 — Jinja2 `min` undefined (500 on `/book/<id>`): FIXED
- `booking.html` line 99 uses `{% for i in range(1, min(tickets_remaining + 1, 11)) %}`
- Jinja2 does not expose Python built-ins by default
- **Fix:** added `app.jinja_env.globals['min'] = min` in `app.py` (line after `mysql = MySQL(app)`)
- This makes `min` available in all templates globally

### Bug 3 — Missing event images (404 on `/static/images/*.jpg`): FIXED
- `static/images/` folder existed but was empty
- Downloaded 6 free placeholder images from picsum.photos:
  - `exhibition.jpg`, `music.jpg`, `sports.jpg`, `theatre.jpg`, `workshop.jpg`, `community.jpg`
- Templates already had `onerror` gradient fallbacks so the site was functional but log was noisy

---

## ✅ Session Log — 16 March 2026 — Review 2 Requirements

### Review 2 criteria fulfilled in `ERD_AND_NORMALIZATION.md`:

**Criterion 1 — ERD complete, 3NF, correct relationships & multiplicities (4 pts): DONE**
- Added a full Mermaid `erDiagram` block at the top of Section 1
- All 8 entities shown with every attribute, PK/FK labelled
- All 8 relationships drawn with correct crow's foot multiplicities (||--o{, ||--o|)
- Fixed BOOKING entity: removed `total_amount` (it was eliminated during 3NF and was not in the SQL — caused a mismatch)

**Criterion 2 — Two examples per normalisation stage (3 pts): DONE**
- 1NF: now has 2 examples (EVENT multi-valued columns + USER non-atomic `full_name`/`contacts` field)
- 2NF: now has 2 examples (BOOKING partial dependencies + TICKET storing redundant event data)
- 3NF: already had 2 examples ✓ (EVENT venue transitive dependency + BOOKING calculated fields)

**Criterion 3 — ERD fully implemented in MySQL, mapped to ERD (3 pts): DONE**
- Added ERD-to-SQL mapping table (Section 4) confirming all 8 entities match `CREATE TABLE` statements in `bristol_events.sql`
- All PKs, FKs, ENUMs, and constraints cross-referenced

**To view the ERD diagram:** Open `ERD_AND_NORMALIZATION.md` in VS Code with the Mermaid Preview extension, or paste the diagram block at [mermaid.live](https://mermaid.live)

---

## Remaining Work — Final Submission (due 23 April 2026)

> Phases 1–4 are complete. The app is fully functional. Below is everything left to do, broken into individual tasks you can tick off.

---

### ✅ PHASE 4 COMPLETE

---

### Phase 5 — Waiting List Page *(~30 mins — backend logic already done)*

The waiting list INSERT/notify logic is already in `app.py`. Only the user-facing page is missing.

- [ ] Add `/waiting-list` GET route to `app.py`
  - Query: `SELECT wl.*, e.event_name, e.start_date, v.venue_name FROM WAITING_LIST wl JOIN EVENT e ... JOIN VENUE v ... WHERE wl.user_id=%s ORDER BY wl.joined_at DESC`
  - Pass results to template
- [ ] Create `templates/waiting_list.html`
  - Table showing: Event name, date, venue, position joined, status (waiting/offered/expired)
  - Link in navbar: visible only when logged in (same as "My Bookings")
- [ ] Add "You're on the waiting list" link/badge to `templates/my_bookings.html` if user has active waiting list entries

---

### Phase 6 — Security Hardening *(~1–2 hrs)*

- [ ] **CSRF protection** — install `flask-wtf`, add to `requirements.txt`
  - Add `app.config['WTF_CSRF_SECRET_KEY']` in `app.py`
  - Add `{{ csrf_token() }}` hidden field to every POST form: `login.html`, `register.html`, `booking.html`, `my_bookings.html` (cancel form), all admin forms
- [ ] **Input validation** (server-side, in `app.py` POST routes)
  - Register: email must contain `@`, password ≥ 8 chars, phone numeric
  - Booking: `num_tickets` must be integer 1–10
  - Admin event form: `start_date` must be in the future, `ticket_price` ≥ 0
- [ ] **Secret key** — move out of source code
  - Create `.env` file: `SECRET_KEY=your-secret-here`
  - Install `python-dotenv`, add `from dotenv import load_dotenv; load_dotenv()` at top of `app.py`
  - Change `app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')`
  - Add `.env` to `.gitignore`

---

### Phase 7 — Polish *(~2–3 hrs — highest mark impact)*

#### 7a — Profile page *(new page)*
- [ ] Add `/profile` GET/POST route to `app.py`
  - GET: `SELECT * FROM USER WHERE user_id=%s`, render form pre-filled
  - POST (details): `UPDATE USER SET first_name, last_name, phone_number WHERE user_id=%s`
  - POST (password): verify old password with `check_password_hash`, then `UPDATE USER SET password_hash WHERE user_id=%s`
- [ ] Create `templates/profile.html`
  - Two sections: "Your Details" form + "Change Password" form
  - Show: first name, last name, email (read-only), phone, is_student checkbox

#### 7b — Booking receipt page *(new page)*
- [ ] Add `/booking-receipt/<id>` GET route to `app.py`
  - Fetch booking + all tickets + event + venue for that booking_id (verify `user_id` matches session)
  - Pass full price breakdown to template
- [ ] Create `templates/booking_receipt.html`
  - Printable layout: booking reference, event name, date, venue, num tickets, base price, discount applied, final amount, list of ticket numbers (`BCE-YEAR-bookingid-N`)
  - "Print" button using `window.print()`
- [ ] Add "View Receipt" link in `my_bookings.html` for each confirmed booking

#### 7c — Event detail improvements
- [ ] Add `conditions` field display to `templates/event_detail.html` (show as a note/callout box if not null)
- [ ] Add `last_booking_date` warning to `templates/event_detail.html` — e.g. "Book by 15 Apr" in amber if within 7 days

#### 7d — Responsiveness check
- [ ] Open browser DevTools → toggle device toolbar
- [ ] Test at 320px (mobile), 768px (tablet), 1200px (desktop)
- [ ] Fix any overflow/wrapping issues in admin tables on mobile

---

### Quick Wins for PR3 Week 21 Demo (due 24 March)
The app already satisfies Week 21 requirements. Just run:
```
python app.py
```
Then visit `http://localhost:5000/events` — events load dynamically from DB ✓

---

## Existing Assets to Keep

| Asset | Status |
|-------|--------|
| `static/css/styles.css` | Keep as-is (954 lines, fully responsive) |
| `static/js/script.js` | Keep as-is (mobile menu, animations, price calc) |
| All URL route names (`/`, `/events`, `/event/<id>`, etc.) | Keep same paths |
| `bristol_events.sql` | Already 3NF — use as the DB schema |
| Password hashing pattern with `werkzeug.security` | Keep, expand to DB |
| Session-based auth pattern | Keep, wire to DB |
| All 9 HTML templates | Refactor Jinja2 variables to match DB query results |

---

## Pre-requisite — MySQL Setup

MySQL is not yet installed. Before any coding:
1. Download and install **XAMPP** (includes MySQL + phpMyAdmin): https://www.apachefriends.org
2. Start the Apache and MySQL modules in the XAMPP Control Panel
3. Open phpMyAdmin at `http://localhost/phpmyadmin`
4. Run `bristol_events.sql` to create the database (Import tab → select file → Go)
5. Verify all 8 tables appear in the `bristol_events` database

---

## Database Schema

Extend the existing `bristol_events.sql` with one additional table for multi-day booking day selections:

**Existing 7 tables (keep as-is):**
- `USER` — user_id, first_name, last_name, email, password_hash, phone_number, is_student, user_type ENUM('standard','admin'), created_at, updated_at
- `VENUE` — venue_id, venue_name, address, capacity, suitable_for
- `EVENT_CATEGORY` — category_id, category_name, description
- `EVENT` — event_id, event_name, event_description, start_date, end_date, ticket_price, is_multi_day, days_count, price_per_day, last_booking_date, conditions, venue_id FK, category_id FK
- `BOOKING` — booking_id, user_id FK, event_id FK, booking_date, number_of_tickets, discount_percentage, student_discount_applied, final_amount, booking_status ENUM('confirmed','cancelled','pending'), cancellation_fee
- `TICKET` — ticket_id, booking_id FK, ticket_number, is_used
- `WAITING_LIST` — waiting_id, user_id FK, event_id FK, joined_at, notified, status ENUM('waiting','offered','expired')
- `PAYMENT` — payment_id, booking_id FK, payment_method, payment_amount, payment_status, transaction_id

**New table to add to bristol_events.sql:**
```sql
CREATE TABLE BOOKING_DAY (
    booking_day_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    day_date DATE NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE,
    UNIQUE KEY unique_booking_day (booking_id, day_date)
);
```
This links a BOOKING to specific days chosen by the user for multi-day events. For single-day events, no BOOKING_DAY rows are needed. The per-day price = `EVENT.price_per_day * number_of_tickets * COUNT(BOOKING_DAY rows)`.

---

## Phase 1 — MySQL Connection & Core Data Layer
**Goal:** Replace hardcoded data with live DB queries; satisfies PR3 Week 21

### Files to modify:
- **`app.py`** — Add Flask-MySQLdb config, replace all SAMPLE_EVENTS/SAMPLE_CATEGORIES/SAMPLE_VENUES with cursor queries
- **`requirements.txt`** — Already has Flask-MySQLdb==1.0.1 and mysqlclient==2.2.0 ✓

### Steps:
1. Add MySQL config to `app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = ''
   app.config['MYSQL_DB'] = 'bristol_events'
   app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
   mysql = MySQL(app)
   ```
2. Replace `/` route — query `SELECT e.*, v.venue_name, ec.category_name, v.capacity, (v.capacity - COALESCE(SUM(b.number_of_tickets),0)) AS tickets_remaining FROM EVENT e JOIN VENUE v ... LEFT JOIN BOOKING b ... WHERE b.booking_status='confirmed' GROUP BY e.event_id LIMIT 3`
3. Replace `/events` route — same join with optional filters (category, date, free_only)
4. Replace `/event/<id>` route — single event by event_id with venue + category
5. Delete `SAMPLE_EVENTS`, `SAMPLE_CATEGORIES`, `SAMPLE_VENUES`, `USERS {}`, `BOOKINGS []` globals

### Template changes:
- Rename dict keys in templates to match DB column names exactly (e.g., `event['event_name']` not `event['name']`, `event['number_of_tickets']` → already matches)
- `events.html`: add filter form (category dropdown, date, free checkbox) — submit GET to `/events`

---

## Phase 2 — User Authentication via DB
**Goal:** Register/login/logout store and read from MySQL; satisfies PR3 Week 22 (form→DB→response)

### Files to modify:
- **`app.py`** — `/register` and `/login` routes

### Steps:
1. **`/register` POST:** `INSERT INTO USER (first_name, last_name, email, password_hash, phone_number, is_student) VALUES (%s,%s,%s,%s,%s,%s)` using parameterized queries
2. **`/login` POST:** `SELECT * FROM USER WHERE email=%s`, then `check_password_hash`; store `session['user_type']` alongside existing session vars
3. Add `is_admin` helper: `session.get('user_type') == 'admin'`
4. Add **`/profile` GET/POST** route — display and update user data (name, phone, password); uses `UPDATE USER SET ... WHERE user_id=%s`
5. Add **password update** sub-form in profile: verify old password, hash new, UPDATE

### Templates to create/modify:
- Modify `register.html` — already correct field names, no changes needed
- Modify `login.html` — already correct
- **New `profile.html`** — user details form + password change section

---

## Phase 3 — Booking System via DB
**Goal:** Full booking flow with real discount logic, stored in MySQL

### Files to modify:
- **`app.py`** — `/book/<id>` GET/POST, `/my-bookings`, new `/cancel-booking/<id>`

### Business logic to implement in Python:

**Advance booking discount** (calculate from today to event start_date):
```python
def get_advance_discount(days_until_event):
    if days_until_event >= 50: return 20
    if days_until_event >= 35: return 15
    if days_until_event >= 25: return 10
    if days_until_event >= 15: return 5
    return 0
```

**Cancellation charge** (calculate from today to event start_date):
```python
def get_cancellation_charge(days_until_event):
    if days_until_event >= 40: return 0
    if days_until_event >= 25: return 40
    return 100  # within 25 days = 100%
```

### Steps:
1. **`/book/<id>` GET:** Calculate `days_until_event`, call `get_advance_discount()`, pass `preview_discount` to template
2. **`/book/<id>` POST:**
   - Check tickets_remaining (capacity minus confirmed bookings) ≥ num_tickets requested
   - Check booking 2 months in advance (start_date ≤ today + 60 days)
   - If event full → redirect to waiting list join
   - Calculate discounts, final_amount
   - `INSERT INTO BOOKING ...` with parameterized query
   - `INSERT INTO TICKET ...` for each ticket (generate ticket numbers `BCE-YEAR-bookingid-N`)
   - Redirect to booking confirmation/my-bookings
3. **`/my-bookings`:** `SELECT b.*, e.event_name, e.start_date, v.venue_name FROM BOOKING b JOIN EVENT e ... JOIN VENUE v ... WHERE b.user_id=%s ORDER BY b.created_at DESC`
4. **`/cancel-booking/<id>` POST:** calculate days until event, apply cancellation_fee, `UPDATE BOOKING SET booking_status='cancelled', cancellation_fee=%s WHERE booking_id=%s AND user_id=%s`
5. **`/booking-receipt/<id>` GET:** fetch booking + tickets + event details, render as printable HTML page with full price breakdown

### Templates to modify:
- `booking.html` — pass `advance_discount` and `student_discount` from Flask; JS `updateSummary()` already handles client-side display ✓
- `my_bookings.html` — add Cancel button (POST form) with cancellation charge warning
- **New `booking_receipt.html`** — printable receipt showing: event, date, venue, num tickets, base price, discounts applied, final amount, ticket numbers, booking reference

---

## Phase 4 — Admin Panel
**Goal:** Admin routes and UI for managing events, venues, users, and reports

**Scope: Core admin only** (covers ~25/30 marks for Element 3)

### New routes in `app.py`:
All protected with `if session.get('user_type') != 'admin': abort(403)`

| Route | Method | Purpose |
|-------|--------|---------|
| `/admin` | GET | Dashboard: summary stats |
| `/admin/events` | GET | List all events with edit/delete |
| `/admin/events/add` | GET/POST | Add new event |
| `/admin/events/edit/<id>` | GET/POST | Edit event |
| `/admin/events/delete/<id>` | POST | Delete event |
| `/admin/venues` | GET/POST | List venues + add new venue inline |
| `/admin/bookings` | GET | View all bookings with filters |
| `/admin/reports` | GET | All reports on one page |

### Reports queries (reuse SQL already in bristol_events.sql):
- **Revenue per event:** `SUM(b.final_amount)` grouped by event_id
- **Bookings count per event:** `COUNT(b.booking_id)` grouped by event_id
- **Tickets remaining per event:** `v.capacity - COALESCE(SUM(b.number_of_tickets),0)`
- **Upcoming events at a specific venue:** filter by venue_id and `start_date >= CURDATE()`

### Templates to create:
- `templates/admin/dashboard.html` — stat cards (events, bookings, revenue, users)
- `templates/admin/events.html` — table with edit/delete links
- `templates/admin/event_form.html` — shared add/edit form (venue + category dropdowns from DB)
- `templates/admin/venues.html` — venues list + inline add form
- `templates/admin/bookings.html` — all bookings table
- `templates/admin/reports.html` — all 4 report tables on one page

---

## Phase 5 — Waiting List
**Goal:** Handle full events gracefully

### Steps:
1. In `/book/<id>` POST: if event full, `INSERT INTO WAITING_LIST (user_id, event_id) VALUES (%s,%s)` and flash "Added to waiting list"
2. In `/cancel-booking/<id>` POST: after cancellation, check `SELECT * FROM WAITING_LIST WHERE event_id=%s AND status='waiting' ORDER BY joined_at LIMIT 1`; if found, update `status='offered'` and flash admin notification
3. **`/waiting-list` GET:** show user's waiting list entries
4. Add waiting list status to `my_bookings.html`

---

## Phase 6 — Security Hardening
**Goal:** SQL injection, XSS, CSRF, input validation

### Steps:
1. **SQL injection:** All DB queries already use parameterized `%s` placeholders — verify no string concatenation in queries
2. **XSS:** Jinja2 auto-escapes by default; add `|e` filter on any `|safe` usages; sanitize user inputs server-side
3. **CSRF:** Add `Flask-WTF` (pip install flask-wtf); use `{{ form.hidden_tag() }}` or manually generate/verify CSRF tokens for all POST forms
4. **Input validation:** Validate email format, password length ≥ 8 chars, phone format, num_tickets 1-10, dates make sense
5. **Secret key:** Move to environment variable or config file (not hardcoded)
6. **Admin check decorator:** Create `@admin_required` decorator to DRY up admin route protection

---

## Phase 7 — Polish & PR1 Completeness
**Goal:** Ensure all pages complete and error-free for full marks

### Steps:
1. Create `templates/base.html` — extract shared nav + footer from all templates to avoid duplication
2. Extend all existing templates with `{% extends 'base.html' %}`
3. Add event **filtering** to `/events`: category dropdown (from DB), date range, free events checkbox
4. Add **image placeholders** or gradient backgrounds where images are missing
5. Add `conditions` field display in `event_detail.html`
6. Add `last_booking_date` display and booking deadline warning
7. Verify responsive breakpoints work at 320px (mobile), 768px (tablet), 1200px (desktop)
8. Test all pages render without errors

---

## Files Modified Summary

| File | Action |
|------|--------|
| `app.py` | Major rewrite — add MySQL, replace all hardcoded data, add 15+ new routes |
| `bristol_events.sql` | Add BOOKING_DAY table |
| `requirements.txt` | Add `flask-wtf` for CSRF |
| `templates/index.html` | Minor — variable names match DB |
| `templates/events.html` | Add filter form |
| `templates/event_detail.html` | Add conditions, last_booking_date |
| `templates/booking.html` | Pass real discounts from Flask; add day-picker for multi-day events |
| `templates/my_bookings.html` | Add cancel button, waiting list entries |
| `templates/register.html` | No changes needed |
| `templates/login.html` | No changes needed |
| `templates/about.html` | No changes needed |
| `templates/contact.html` | No changes needed |
| `templates/base.html` | **New** — shared nav/footer |
| `templates/profile.html` | **New** — user profile + password update |
| `templates/booking_receipt.html` | **New** — printable receipt |
| `templates/waiting_list.html` | **New** |
| `templates/admin/dashboard.html` | **New** |
| `templates/admin/events.html` | **New** |
| `templates/admin/event_form.html` | **New** |
| `templates/admin/venues.html` | **New** |
| `templates/admin/bookings.html` | **New** |
| `templates/admin/reports.html` | **New** |

---

## Verification

1. Start XAMPP, enable MySQL, run `bristol_events.sql` via phpMyAdmin
2. Install dependencies: `pip install -r requirements.txt`
3. Start Flask: `python app.py`
4. **PR3 Week 21 check:** Visit `/events` — events load from DB with venue/category names ✓
5. **PR3 Week 22 check:** Register new user → appears in MySQL USER table ✓
6. Test booking flow: login → browse → book → check my-bookings → cancel
7. Test admin: login as `admin@bristolevents.com` → `/admin` dashboard loads ✓
8. Test discounts: book event 50+ days away → 20% discount shown ✓
9. Test cancellation charges: cancel within 25 days → 100% charge applied ✓
10. Test waiting list: book fully-booked event → added to waiting list ✓
11. Test reports: `/admin/reports` shows revenue per event, booking counts ✓
12. Test responsiveness at 320px, 768px, 1200px in browser dev tools


# ebadi notes
admin@bristolevents.com / Admin123!
