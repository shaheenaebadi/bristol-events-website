-- =====================================================
-- BRISTOL EVENTS MANAGEMENT SYSTEM - SQL DATABASE
-- Student ID: [Your Student ID]
-- Date: January 2026
-- Database in 3rd Normal Form (3NF)
-- =====================================================

-- Create Database
DROP DATABASE IF EXISTS bristol_events;
CREATE DATABASE bristol_events;
USE bristol_events;

-- =====================================================
-- TABLE CREATION
-- =====================================================

-- Table: USER
CREATE TABLE USER (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    is_student BOOLEAN DEFAULT FALSE,
    user_type ENUM('standard', 'admin') DEFAULT 'standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_user_type (user_type)
);

-- Table: VENUE
CREATE TABLE VENUE (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
    suitable_for VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (capacity > 0)
);

-- Table: EVENT_CATEGORY
CREATE TABLE EVENT_CATEGORY (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Table: EVENT
CREATE TABLE EVENT (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(150) NOT NULL,
    event_description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    is_multi_day BOOLEAN DEFAULT FALSE,
    days_count INT DEFAULT 1,
    price_per_day DECIMAL(10, 2),
    last_booking_date DATE,
    conditions TEXT,
    venue_id INT NOT NULL,
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (venue_id) REFERENCES VENUE(venue_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES EVENT_CATEGORY(category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (end_date >= start_date),
    CHECK (ticket_price >= 0),
    CHECK (days_count > 0),
    INDEX idx_start_date (start_date),
    INDEX idx_venue (venue_id),
    INDEX idx_category (category_id)
);

-- Table: BOOKING
CREATE TABLE BOOKING (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    booking_date DATE NOT NULL,
    number_of_tickets INT NOT NULL DEFAULT 1,
    discount_percentage DECIMAL(5, 2) DEFAULT 0.00,
    student_discount_applied BOOLEAN DEFAULT FALSE,
    final_amount DECIMAL(10, 2) NOT NULL,
    booking_status ENUM('confirmed', 'cancelled', 'pending') DEFAULT 'pending',
    cancellation_fee DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (number_of_tickets > 0),
    CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    CHECK (final_amount >= 0),
    INDEX idx_user (user_id),
    INDEX idx_event (event_id),
    INDEX idx_booking_date (booking_date),
    INDEX idx_status (booking_status)
);

-- Table: TICKET
CREATE TABLE TICKET (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    check_in_time TIMESTAMP NULL,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_booking (booking_id),
    INDEX idx_ticket_number (ticket_number)
);

-- Table: WAITING_LIST
CREATE TABLE WAITING_LIST (
    waiting_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notified BOOLEAN DEFAULT FALSE,
    status ENUM('waiting', 'offered', 'expired') DEFAULT 'waiting',
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_waiting (user_id),
    INDEX idx_event_waiting (event_id),
    INDEX idx_status_waiting (status)
);

-- Table: PAYMENT
CREATE TABLE PAYMENT (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL UNIQUE,
    payment_method VARCHAR(50) NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (payment_amount >= 0),
    INDEX idx_booking_payment (booking_id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_payment_status (payment_status)
);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert Event Categories
INSERT INTO EVENT_CATEGORY (category_name, description) VALUES
('Exhibition', 'Art, culture, and creative displays'),
('Workshop', 'Educational and skill-building sessions'),
('Sports', 'Sporting events and competitions'),
('Musical', 'Live music performances and concerts'),
('Theatre', 'Theatrical performances and plays'),
('Religious', 'Religious celebrations and ceremonies'),
('Community', 'Community gatherings and festivals');

-- Insert Venues
INSERT INTO VENUE (venue_name, address, capacity, suitable_for) VALUES
('Ashton Gate Stadium', 'Ashton Road, Bristol BS3 2EJ', 150, 'Musical, Sports, Exhibitions'),
('Arnolfini', '16 Narrow Quay, Bristol BS1 4QA', 100, 'Exhibitions, Workshops'),
('The Bristol Hippodrome', 'St Augustines Parade, Bristol BS1 4UZ', 120, 'Theatre, Musical'),
('Bristol Old Vic', 'King Street, Bristol BS1 4ED', 110, 'Theatre'),
('Bristol Central Library', 'College Green, Bristol BS1 5TL', 50, 'Exhibitions'),
('Royal West of England Academy', 'Queens Road, Clifton, Bristol BS8 1PX', 100, 'Exhibitions'),
('Creative Space A', '10 Workshop Lane, Bristol BS2 9XY', 30, 'Workshops'),
('Creative Space B', '25 Artisan Street, Bristol BS2 8LD', 50, 'Workshops, Courses'),
('UWE Exhibition Centre', 'Frenchay Campus, Bristol BS16 1QY', 300, 'Weddings, Workshops, Conferences, Exhibitions'),
('Community Centre A', '45 Community Road, Bristol BS4 3RF', 60, 'Private events, Religious events');

-- Insert Users (Admin and Standard Users)
INSERT INTO USER (first_name, last_name, email, password_hash, phone_number, is_student, user_type) VALUES
('Admin', 'User', 'admin@bristolevents.com', 'hashed_password_admin', '+44117000001', FALSE, 'admin'),
('John', 'Smith', 'john.smith@email.com', 'hashed_password_1', '+44117123456', FALSE, 'standard'),
('Emma', 'Johnson', 'emma.j@email.com', 'hashed_password_2', '+44117234567', TRUE, 'standard'),
('Michael', 'Williams', 'mike.w@email.com', 'hashed_password_3', '+44117345678', FALSE, 'standard'),
('Sarah', 'Brown', 'sarah.b@email.com', 'hashed_password_4', '+44117456789', TRUE, 'standard'),
('David', 'Jones', 'david.jones@email.com', 'hashed_password_5', '+44117567890', FALSE, 'standard'),
('Lisa', 'Taylor', 'lisa.t@email.com', 'hashed_password_6', '+44117678901', TRUE, 'standard'),
('James', 'Davies', 'james.d@email.com', 'hashed_password_7', '+44117789012', FALSE, 'standard');

-- Insert Events
INSERT INTO EVENT (event_name, event_description, start_date, end_date, ticket_price, is_multi_day, days_count, price_per_day, last_booking_date, conditions, venue_id, category_id) VALUES
('Bristol Balloon Fiesta', 'A spectacular week of hot air balloons, rides, and family entertainment', '2026-05-03', '2026-05-10', 70.00, TRUE, 7, 10.00, '2026-04-28', 'Suitable for all ages', 1, 7),
('Contemporary Art Exhibition', 'Explore modern art from local and international artists', '2026-05-08', '2026-05-08', 0.00, FALSE, 1, 0.00, '2026-05-06', 'Free entry with booking', 2, 1),
('Bristol City FC vs Leeds United', 'Exciting Championship football match', '2026-05-12', '2026-05-12', 50.00, FALSE, 1, 50.00, '2026-05-10', 'Stadium seating', 1, 3),
('Shakespeare''s Hamlet', 'Classic theatrical performance by Bristol Old Vic Company', '2026-05-16', '2026-05-16', 35.00, FALSE, 1, 35.00, '2026-05-14', 'Formal attire recommended', 4, 5),
('Bristol Jazz Festival', 'Three days of world-class jazz performances', '2026-05-21', '2026-05-23', 45.00, TRUE, 3, 15.00, '2026-05-19', 'All ages welcome', 3, 4),
('Digital Photography Workshop', 'Learn professional photography techniques', '2026-05-28', '2026-05-28', 25.00, FALSE, 1, 25.00, '2026-05-26', 'Bring your own camera', 7, 2),
('Spring Art Fair', 'Annual exhibition of local artists'' work', '2026-06-04', '2026-06-06', 0.00, TRUE, 3, 0.00, '2026-06-02', 'Free admission', 6, 1),
('Bristol Marathon', 'Annual city marathon event', '2026-06-11', '2026-06-11', 30.00, FALSE, 1, 30.00, '2026-06-06', 'Participants only', 1, 3),
('Classical Music Concert', 'Symphony orchestra performance', '2026-06-18', '2026-06-18', 40.00, FALSE, 1, 40.00, '2026-06-16', 'Smart casual dress code', 3, 4),
('Pottery Making Workshop', 'Hands-on pottery and ceramics workshop', '2026-06-25', '2026-06-25', 30.00, FALSE, 1, 30.00, '2026-06-23', 'All materials provided', 8, 2);

-- Insert Bookings
INSERT INTO BOOKING (user_id, event_id, booking_date, number_of_tickets, discount_percentage, student_discount_applied, final_amount, booking_status) VALUES
(2, 1, '2026-03-07', 2, 20.00, FALSE, 112.00, 'confirmed'), -- Booked 57 days in advance (20% discount)
(3, 2, '2026-04-18', 1, 10.00, TRUE, 0.00, 'confirmed'), -- Student, free event
(4, 3, '2026-04-11', 3, 15.00, FALSE, 127.50, 'confirmed'), -- Booked 31 days in advance (15% discount)
(5, 4, '2026-04-06', 2, 10.00, TRUE, 63.00, 'confirmed'), -- Student discount (10%) + early bird (10%)
(6, 5, '2026-05-08', 1, 5.00, FALSE, 42.75, 'pending'), -- Booked 13 days in advance (5% discount)
(7, 6, '2026-05-13', 1, 10.00, TRUE, 22.50, 'confirmed'), -- Student discount
(2, 7, '2026-04-18', 4, 0.00, FALSE, 0.00, 'confirmed'), -- Free event
(3, 8, '2026-05-15', 1, 10.00, TRUE, 27.00, 'pending'); -- Student discount

-- Insert Tickets
INSERT INTO TICKET (booking_id, ticket_number, is_used) VALUES
(1, 'BCE-2026-001-001', FALSE),
(1, 'BCE-2026-001-002', FALSE),
(2, 'BCE-2026-002-001', FALSE),
(3, 'BCE-2026-003-001', FALSE),
(3, 'BCE-2026-003-002', FALSE),
(3, 'BCE-2026-003-003', FALSE),
(4, 'BCE-2026-004-001', FALSE),
(4, 'BCE-2026-004-002', FALSE),
(5, 'BCE-2026-005-001', FALSE),
(6, 'BCE-2026-006-001', FALSE),
(7, 'BCE-2026-007-001', FALSE),
(7, 'BCE-2026-007-002', FALSE),
(7, 'BCE-2026-007-003', FALSE),
(7, 'BCE-2026-007-004', FALSE),
(8, 'BCE-2026-008-001', FALSE);

-- Insert Waiting List entries
INSERT INTO WAITING_LIST (user_id, event_id, status) VALUES
(6, 1, 'waiting'),
(7, 3, 'waiting'),
(4, 5, 'offered');

-- Insert Payments
INSERT INTO PAYMENT (booking_id, payment_method, payment_amount, payment_status, transaction_id) VALUES
(1, 'Credit Card', 112.00, 'completed', 'TXN-2026-03-07-001'),
(2, 'Credit Card', 0.00, 'completed', 'TXN-2026-04-18-002'),
(3, 'PayPal', 127.50, 'completed', 'TXN-2026-04-11-003'),
(4, 'Credit Card', 63.00, 'completed', 'TXN-2026-04-06-004'),
(5, 'Debit Card', 42.75, 'pending', 'TXN-2026-05-08-005'),
(6, 'Credit Card', 22.50, 'completed', 'TXN-2026-05-13-006'),
(7, 'Credit Card', 0.00, 'completed', 'TXN-2026-04-18-007'),
(8, 'PayPal', 27.00, 'pending', 'TXN-2026-05-15-008');

-- =====================================================
-- USEFUL QUERIES FOR VERIFICATION
-- =====================================================

-- View all events with venue and category information
SELECT 
    e.event_name,
    e.start_date,
    e.ticket_price,
    v.venue_name,
    v.capacity,
    ec.category_name
FROM EVENT e
JOIN VENUE v ON e.venue_id = v.venue_id
JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
ORDER BY e.start_date;

-- View all bookings with user and event details
SELECT 
    u.first_name,
    u.last_name,
    e.event_name,
    b.booking_date,
    b.number_of_tickets,
    b.final_amount,
    b.booking_status
FROM BOOKING b
JOIN USER u ON b.user_id = u.user_id
JOIN EVENT e ON b.event_id = e.event_id
ORDER BY b.booking_date DESC;

-- Calculate total tickets available for each event
SELECT 
    e.event_name,
    v.capacity AS total_capacity,
    COALESCE(SUM(b.number_of_tickets), 0) AS tickets_booked,
    v.capacity - COALESCE(SUM(b.number_of_tickets), 0) AS tickets_remaining
FROM EVENT e
JOIN VENUE v ON e.venue_id = v.venue_id
LEFT JOIN BOOKING b ON e.event_id = b.event_id AND b.booking_status = 'confirmed'
GROUP BY e.event_id, e.event_name, v.capacity;

-- Admin Report: Revenue per event
SELECT 
    e.event_name,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.number_of_tickets) AS tickets_sold,
    SUM(b.final_amount) AS total_revenue
FROM EVENT e
LEFT JOIN BOOKING b ON e.event_id = b.event_id AND b.booking_status = 'confirmed'
GROUP BY e.event_id, e.event_name
ORDER BY total_revenue DESC;

-- Users on waiting list
SELECT 
    u.first_name,
    u.last_name,
    e.event_name,
    wl.joined_at,
    wl.status
FROM WAITING_LIST wl
JOIN USER u ON wl.user_id = u.user_id
JOIN EVENT e ON wl.event_id = e.event_id
WHERE wl.status = 'waiting'
ORDER BY wl.joined_at;

-- Upcoming events (next 30 days)
SELECT 
    e.event_name,
    e.start_date,
    e.ticket_price,
    v.venue_name,
    ec.category_name,
    v.capacity - COALESCE(SUM(b.number_of_tickets), 0) AS tickets_available
FROM EVENT e
JOIN VENUE v ON e.venue_id = v.venue_id
JOIN EVENT_CATEGORY ec ON e.category_id = ec.category_id
LEFT JOIN BOOKING b ON e.event_id = b.event_id AND b.booking_status = 'confirmed'
WHERE e.start_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
GROUP BY e.event_id
ORDER BY e.start_date;

-- Student bookings summary
SELECT 
    CONCAT(u.first_name, ' ', u.last_name) AS student_name,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.final_amount) AS total_spent,
    SUM(b.number_of_tickets) AS total_tickets
FROM USER u
JOIN BOOKING b ON u.user_id = b.user_id
WHERE u.is_student = TRUE AND b.booking_status = 'confirmed'
GROUP BY u.user_id
ORDER BY total_spent DESC;

-- =====================================================
-- DATABASE INTEGRITY VERIFICATION
-- =====================================================

-- Check for referential integrity
SELECT 
    'All EVENT records reference valid VENUE' AS check_description,
    COUNT(*) AS count
FROM EVENT e
LEFT JOIN VENUE v ON e.venue_id = v.venue_id
WHERE v.venue_id IS NULL;

SELECT 
    'All BOOKING records reference valid USER and EVENT' AS check_description,
    COUNT(*) AS count
FROM BOOKING b
LEFT JOIN USER u ON b.user_id = u.user_id
LEFT JOIN EVENT e ON b.event_id = e.event_id
WHERE u.user_id IS NULL OR e.event_id IS NULL;

-- =====================================================
-- END OF SQL SCRIPT
-- =====================================================
