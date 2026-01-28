# BRISTOL EVENTS MANAGEMENT SYSTEM - DATABASE DESIGN
## Student ID: [Your Student ID]
## Date: January 2026

---

## 1. ENTITY RELATIONSHIP DIAGRAM (ERD)

### Entities Identified:

1. **USER**
   - user_id (PK)
   - first_name
   - last_name
   - email
   - password_hash
   - phone_number
   - is_student
   - user_type (standard/admin)
   - created_at
   - updated_at

2. **VENUE**
   - venue_id (PK)
   - venue_name
   - address
   - capacity
   - suitable_for (event types)
   - created_at
   - updated_at

3. **EVENT_CATEGORY**
   - category_id (PK)
   - category_name (Exhibition, Workshop, Sports, Musical, Theatre, Religious, Community)
   - description

4. **EVENT**
   - event_id (PK)
   - event_name
   - event_description
   - start_date
   - end_date
   - ticket_price
   - is_multi_day
   - days_count
   - price_per_day
   - last_booking_date
   - conditions (e.g., formal dress)
   - venue_id (FK)
   - category_id (FK)
   - created_at
   - updated_at

5. **BOOKING**
   - booking_id (PK)
   - user_id (FK)
   - event_id (FK)
   - booking_date
   - number_of_tickets
   - total_amount
   - discount_percentage
   - student_discount_applied
   - final_amount
   - booking_status (confirmed/cancelled/pending)
   - cancellation_fee
   - created_at
   - updated_at

6. **TICKET**
   - ticket_id (PK)
   - booking_id (FK)
   - ticket_number
   - is_used
   - check_in_time

7. **WAITING_LIST**
   - waiting_id (PK)
   - user_id (FK)
   - event_id (FK)
   - joined_at
   - notified
   - status (waiting/offered/expired)

8. **PAYMENT**
   - payment_id (PK)
   - booking_id (FK)
   - payment_method
   - payment_amount
   - payment_status
   - transaction_id
   - payment_date

---

## 2. RELATIONSHIPS

1. **USER to BOOKING**: One-to-Many
   - One user can make multiple bookings
   - Each booking is made by one user

2. **EVENT to BOOKING**: One-to-Many
   - One event can have multiple bookings
   - Each booking is for one event

3. **VENUE to EVENT**: One-to-Many
   - One venue can host multiple events
   - Each event is held at one venue

4. **EVENT_CATEGORY to EVENT**: One-to-Many
   - One category can have multiple events
   - Each event belongs to one category

5. **BOOKING to TICKET**: One-to-Many
   - One booking can have multiple tickets
   - Each ticket belongs to one booking

6. **USER to WAITING_LIST**: One-to-Many
   - One user can be on waiting lists for multiple events
   - Each waiting list entry is for one user

7. **EVENT to WAITING_LIST**: One-to-Many
   - One event can have multiple users on waiting list
   - Each waiting list entry is for one event

8. **BOOKING to PAYMENT**: One-to-One
   - Each booking has one payment record
   - Each payment record is for one booking

---

## 3. NORMALIZATION PROCESS

### 3.1 FIRST NORMAL FORM (1NF)

**Requirements for 1NF:**
- Eliminate repeating groups
- Each cell contains single atomic value
- Each record is unique

**Example showing why the database is in 1NF:**

**Before 1NF (Unnormalized):**
```
EVENT_TABLE:
| event_id | event_name | venues | categories | dates |
|----------|------------|--------|-----------|-------|
| 1 | Balloon Fiesta | Ashton Court | Festival, Musical | 15-Feb, 16-Feb, 17-Feb |
```

**Problem:** Multiple values in 'venues', 'categories', and 'dates' columns

**After 1NF:**
```
EVENT:
| event_id | event_name | venue_id | category_id | start_date | end_date |
|----------|------------|----------|-------------|------------|----------|
| 1 | Balloon Fiesta | 1 | 1 | 15-Feb | 22-Feb |
```

**Changes Made:**
1. Split multi-valued attributes into separate columns
2. Created separate VENUE and EVENT_CATEGORY tables
3. Each field contains only atomic values
4. Date range replaced with start_date and end_date

---

### 3.2 SECOND NORMAL FORM (2NF)

**Requirements for 2NF:**
- Must be in 1NF
- All non-key attributes must be fully dependent on primary key
- No partial dependencies

**Example showing transformation to 2NF:**

**Before 2NF (Has Partial Dependency):**
```
BOOKING_TABLE:
| booking_id | user_id | event_id | user_email | event_name | booking_date | amount |
|------------|---------|----------|------------ |------------|--------------|--------|
| 1 | 101 | 1 | user@email.com | Balloon Fiesta | 01-Jan | 70.00 |
```

**Problem:** 
- user_email depends only on user_id (not full primary key)
- event_name depends only on event_id (not full primary key)
- These are partial dependencies

**After 2NF:**

**USER Table:**
```
| user_id | first_name | last_name | email | phone_number |
|---------|-----------|-----------|-------|--------------|
| 101 | John | Smith | user@email.com | +44123456 |
```

**EVENT Table:**
```
| event_id | event_name | venue_id | category_id | ticket_price |
|----------|------------|----------|-------------|--------------|
| 1 | Balloon Fiesta | 1 | 1 | 70.00 |
```

**BOOKING Table:**
```
| booking_id | user_id | event_id | booking_date | final_amount |
|------------|---------|----------|--------------|--------------|
| 1 | 101 | 1 | 01-Jan | 70.00 |
```

**Changes Made:**
1. Removed user_email from BOOKING (moved to USER table)
2. Removed event_name from BOOKING (moved to EVENT table)
3. All non-key attributes now fully depend on the primary key

---

### 3.3 THIRD NORMAL FORM (3NF)

**Requirements for 3NF:**
- Must be in 2NF
- No transitive dependencies
- Non-key attributes must not depend on other non-key attributes

**Example showing transformation to 3NF:**

**Before 3NF (Has Transitive Dependency):**
```
EVENT_TABLE:
| event_id | event_name | venue_id | venue_name | venue_address | venue_capacity |
|----------|------------|----------|------------|---------------|----------------|
| 1 | Balloon Fiesta | 1 | Ashton Gate | Bristol | 150 |
```

**Problem:**
- venue_name depends on venue_id (not event_id)
- venue_address depends on venue_id (not event_id)
- venue_capacity depends on venue_id (not event_id)
- This is a transitive dependency: event_id → venue_id → venue_attributes

**After 3NF:**

**EVENT Table:**
```
| event_id | event_name | start_date | end_date | ticket_price | venue_id | category_id |
|----------|------------|------------|----------|--------------|----------|-------------|
| 1 | Balloon Fiesta | 15-Feb | 22-Feb | 70.00 | 1 | 1 |
```

**VENUE Table:**
```
| venue_id | venue_name | address | capacity | suitable_for |
|----------|------------|---------|----------|--------------|
| 1 | Ashton Gate | Bristol Road, BS1 | 150 | Musical, Sports |
```

**Changes Made:**
1. Created separate VENUE table
2. Removed all venue-related attributes from EVENT table
3. Kept only venue_id as foreign key in EVENT table
4. Eliminated transitive dependency

**Another Example - BOOKING with calculated fields:**

**Before 3NF:**
```
BOOKING_TABLE:
| booking_id | user_id | event_id | ticket_price | num_tickets | discount_pct | total | discount_amt | final_amt |
|------------|---------|----------|--------------|-------------|--------------|-------|--------------|-----------|
| 1 | 101 | 1 | 70.00 | 2 | 15 | 140.00 | 21.00 | 119.00 |
```

**Problem:**
- total_amount = ticket_price * num_tickets (derived)
- discount_amount = total_amount * discount_pct (derived)
- final_amount = total_amount - discount_amount (derived)
- These are transitive dependencies

**After 3NF:**
```
BOOKING_TABLE:
| booking_id | user_id | event_id | booking_date | number_of_tickets | discount_percentage | final_amount |
|------------|---------|----------|--------------|-------------------|---------------------|--------------|
| 1 | 101 | 1 | 01-Jan | 2 | 15 | 119.00 |
```

**Changes Made:**
1. Removed calculated fields (total_amount, discount_amount)
2. These can be calculated when needed: 
   - total = ticket_price (from EVENT) * number_of_tickets
   - discount = total * discount_percentage / 100
   - final = total - discount

---

## 4. FINAL DATABASE SCHEMA IN 3NF

### Table: USER
- user_id INT PRIMARY KEY AUTO_INCREMENT
- first_name VARCHAR(50)
- last_name VARCHAR(50)
- email VARCHAR(100) UNIQUE
- password_hash VARCHAR(255)
- phone_number VARCHAR(20)
- is_student BOOLEAN DEFAULT FALSE
- user_type ENUM('standard', 'admin') DEFAULT 'standard'
- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Table: VENUE
- venue_id INT PRIMARY KEY AUTO_INCREMENT
- venue_name VARCHAR(100)
- address VARCHAR(255)
- capacity INT
- suitable_for VARCHAR(255)
- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Table: EVENT_CATEGORY
- category_id INT PRIMARY KEY AUTO_INCREMENT
- category_name VARCHAR(50)
- description TEXT

### Table: EVENT
- event_id INT PRIMARY KEY AUTO_INCREMENT
- event_name VARCHAR(150)
- event_description TEXT
- start_date DATE
- end_date DATE
- ticket_price DECIMAL(10, 2)
- is_multi_day BOOLEAN DEFAULT FALSE
- days_count INT DEFAULT 1
- price_per_day DECIMAL(10, 2)
- last_booking_date DATE
- conditions TEXT
- venue_id INT (FK → VENUE)
- category_id INT (FK → EVENT_CATEGORY)
- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Table: BOOKING
- booking_id INT PRIMARY KEY AUTO_INCREMENT
- user_id INT (FK → USER)
- event_id INT (FK → EVENT)
- booking_date DATE
- number_of_tickets INT
- discount_percentage DECIMAL(5, 2) DEFAULT 0
- student_discount_applied BOOLEAN DEFAULT FALSE
- final_amount DECIMAL(10, 2)
- booking_status ENUM('confirmed', 'cancelled', 'pending') DEFAULT 'pending'
- cancellation_fee DECIMAL(10, 2) DEFAULT 0
- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Table: TICKET
- ticket_id INT PRIMARY KEY AUTO_INCREMENT
- booking_id INT (FK → BOOKING)
- ticket_number VARCHAR(50) UNIQUE
- is_used BOOLEAN DEFAULT FALSE
- check_in_time TIMESTAMP NULL

### Table: WAITING_LIST
- waiting_id INT PRIMARY KEY AUTO_INCREMENT
- user_id INT (FK → USER)
- event_id INT (FK → EVENT)
- joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- notified BOOLEAN DEFAULT FALSE
- status ENUM('waiting', 'offered', 'expired') DEFAULT 'waiting'

### Table: PAYMENT
- payment_id INT PRIMARY KEY AUTO_INCREMENT
- booking_id INT (FK → BOOKING)
- payment_method VARCHAR(50)
- payment_amount DECIMAL(10, 2)
- payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending'
- transaction_id VARCHAR(100)
- payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

---

## 5. SUMMARY OF NORMALIZATION

The Bristol Events database is now in **3rd Normal Form (3NF)** because:

1. **1NF Compliance:**
   - All attributes contain only atomic values
   - No repeating groups
   - Each record has a unique identifier (primary key)

2. **2NF Compliance:**
   - Database is in 1NF
   - All non-key attributes are fully functionally dependent on the primary key
   - No partial dependencies exist

3. **3NF Compliance:**
   - Database is in 2NF
   - No transitive dependencies
   - Non-key attributes depend only on the primary key
   - Derived/calculated values are not stored (can be computed when needed)

This design eliminates redundancy, ensures data integrity, and provides efficient storage and retrieval of information for the Bristol Events Management System.
