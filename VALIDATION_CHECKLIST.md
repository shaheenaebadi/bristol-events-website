# BRISTOL EVENTS - PROGRESS REVIEW VALIDATION CHECKLIST

## Student Information
- **Student ID:** [Your Student ID]
- **Module:** UFCFES-30-1 - Web Development and Databases
- **Date:** January 28, 2026

---

## WEEK 8 - REVIEW POINT 1 (HTML/CSS)
**Maximum Marks: 10**

### Checklist for Tutor Review:

#### 1. Web Pages for All Information Needs (1.5 marks)
- [ ] Homepage (index.html) with hero section and featured events
- [ ] Events browsing page (events.html) with filtering options
- [ ] Event detail page (event-detail.html) with full information
- [ ] Login/Registration page (login.html) with both forms
- [ ] About us page (about.html) with mission and values
- [ ] Contact page (contact.html) with form and details

**Verification:** Open each page in browser and check content is appropriate

---

#### 2. Creative HTML Tags, Logical Flow, All Pages Linked (2.5 marks)

**HTML Tags Used:**
- [ ] Semantic HTML5: `<nav>`, `<section>`, `<footer>`, `<header>`
- [ ] Forms with proper `<input>`, `<select>`, `<textarea>` elements
- [ ] Lists: `<ul>`, `<li>` for navigation and content
- [ ] Proper heading hierarchy: `<h1>`, `<h2>`, `<h3>`
- [ ] Divs with semantic classes for layout

**Logical Flow:**
- [ ] Clear navigation structure across all pages
- [ ] Hero section → Features → Events → Footer (homepage)
- [ ] Consistent layout and structure

**All Pages Linked:**
- [ ] Navigation menu links to all pages
- [ ] Logo links back to homepage
- [ ] Footer contains all links
- [ ] No broken links (test each link)

**Verification:** Click through every link on every page

---

#### 3. Responsive on Three Screen Sizes (2.5 marks)

**Mobile (< 768px):**
- [ ] Hamburger menu appears
- [ ] Single column layout for all content
- [ ] Cards stack vertically
- [ ] Forms adapt to narrow width
- [ ] Text remains readable

**Tablet (768px - 1023px):**
- [ ] Full navigation menu visible
- [ ] Two-column grid layouts
- [ ] Cards display in 2 columns
- [ ] Forms use two-column layout where appropriate

**Desktop (≥ 1024px):**
- [ ] Full navigation menu
- [ ] Three or four-column grids
- [ ] Maximum width constraint (1200px)
- [ ] Optimal use of screen space

**How to Test:**
1. Open index.html in Chrome/Firefox
2. Press F12 (Developer Tools)
3. Click device toolbar icon (Ctrl+Shift+M)
4. Test these exact sizes:
   - 375px (iPhone)
   - 768px (iPad)
   - 1024px (Desktop)
   - 1440px (Large Desktop)

**Verification:** Check all pages at all three breakpoints

---

#### 4. Nice Look & Feel (2.5 marks)

**Color Contrast:**
- [ ] Purple gradient primary color (#667eea to #764ba2)
- [ ] White background for content areas
- [ ] Dark text (#333) on light backgrounds
- [ ] Colored text is readable

**Text Legibility:**
- [ ] Font size: 16px base
- [ ] Line height: 1.6
- [ ] Font family: Segoe UI (professional and readable)
- [ ] Proper spacing between paragraphs

**Images:**
- [ ] Gradient placeholders for event images
- [ ] Icons (emoji) for categories and features
- [ ] Consistent image aspect ratios

**Layout:**
- [ ] Grid-based layouts for cards
- [ ] Consistent padding and margins
- [ ] Card-based design with shadows
- [ ] Proper alignment

**Easy to Navigate:**
- [ ] Sticky navigation bar
- [ ] Clear call-to-action buttons
- [ ] Hover effects on interactive elements
- [ ] Consistent color scheme throughout
- [ ] Footer present on all pages

**Verification:** Does it look professional? Is it easy to read and use?

---

#### 5. Website Syntax is Validated (1 mark)

**HTML Validation:**
- [ ] No syntax errors in HTML
- [ ] Proper DOCTYPE declaration
- [ ] All tags properly closed
- [ ] Valid HTML5 structure

**CSS Validation:**
- [ ] No CSS syntax errors
- [ ] Proper property values
- [ ] Browser-compatible CSS

**No Console Errors:**
- [ ] Open browser console (F12 → Console)
- [ ] No JavaScript errors
- [ ] No missing file errors

**How to Validate:**
1. Visit https://validator.w3.org/
2. Choose "Validate by File Upload"
3. Upload each HTML file
4. Check for errors

**Verification:** All pages should validate with no errors or warnings

---

## TERM 2 - WEEK 2 REVIEW POINT (DATABASE)
**Maximum Marks: 10**

### Checklist for Tutor Review:

#### 1. Database ERD Showing All Requirements (3 marks)

**ERD Location:** `database/ERD_AND_NORMALIZATION.md`

- [ ] All entities clearly identified (8 tables)
- [ ] All attributes listed for each entity
- [ ] Data types specified
- [ ] Primary keys marked (PK)
- [ ] Foreign keys marked (FK)
- [ ] Relationships clearly shown
- [ ] Cardinality/multiplicity indicated
- [ ] Covers full scope of case study

**Entities to Check:**
1. USER
2. VENUE
3. EVENT_CATEGORY
4. EVENT
5. BOOKING
6. TICKET
7. WAITING_LIST
8. PAYMENT

**Verification:** Read ERD_AND_NORMALIZATION.md section 1 and 2

---

#### 2. Database in 1NF with Examples (1 mark)

**Location:** `database/ERD_AND_NORMALIZATION.md` Section 3.1

- [ ] Explanation of 1NF requirements
- [ ] "Before 1NF" example showing unnormalized data
- [ ] "After 1NF" example showing transformation
- [ ] Clear explanation of changes made
- [ ] Shows elimination of repeating groups
- [ ] Shows atomic values

**Key Example:** EVENT table with multi-valued attributes split

**Verification:** Section 3.1 contains clear before/after examples

---

#### 3. Database in 2NF (1 mark)

**Location:** `database/ERD_AND_NORMALIZATION.md` Section 3.2

- [ ] Database is in 1NF
- [ ] No partial dependencies exist
- [ ] All non-key attributes depend on full primary key
- [ ] Proper table structure

**Verification:** All tables have proper primary keys and no partial dependencies

---

#### 4. Show 2NF Transformation Examples (1 mark)

**Location:** `database/ERD_AND_NORMALIZATION.md` Section 3.2

- [ ] "Before 2NF" example showing partial dependency
- [ ] Problem clearly identified
- [ ] "After 2NF" example showing separated tables
- [ ] Explanation of changes made
- [ ] Shows how partial dependencies were removed

**Key Example:** BOOKING table with user_email and event_name removed

**Verification:** Section 3.2 has detailed transformation examples

---

#### 5. Database in 3NF (1 mark)

**Location:** `database/ERD_AND_NORMALIZATION.md` Section 3.3

- [ ] Database is in 2NF
- [ ] No transitive dependencies
- [ ] Non-key attributes depend only on primary key
- [ ] Proper separation of concerns

**Verification:** All tables maintain 3NF with no transitive dependencies

---

#### 6. Show 3NF Transformation Examples (1 mark)

**Location:** `database/ERD_AND_NORMALIZATION.md` Section 3.3

- [ ] "Before 3NF" examples showing transitive dependencies
- [ ] Problems clearly identified
- [ ] "After 3NF" examples with separate tables
- [ ] Multiple examples provided
- [ ] Clear explanation of transformations

**Key Examples:**
1. EVENT table with venue details (transitive dependency)
2. BOOKING table with calculated fields (derived data)

**Verification:** Section 3.3 contains at least 2 detailed examples

---

#### 7. Error-Free SQL with Referential Integrity (2 marks)

**Location:** `database/bristol_events.sql`

**SQL Script Should Contain:**
- [ ] DROP and CREATE DATABASE statements
- [ ] All 8 table CREATE statements
- [ ] Primary key constraints on all tables
- [ ] Foreign key constraints with proper references
- [ ] CHECK constraints where appropriate
- [ ] UNIQUE constraints where needed
- [ ] Indexes for optimization
- [ ] ON DELETE and ON UPDATE actions specified

**Sample Data:**
- [ ] INSERT statements for all tables
- [ ] Data respects all constraints
- [ ] Foreign keys reference existing records
- [ ] Realistic sample data

**Verification Queries:**
- [ ] SELECT queries to verify data
- [ ] Queries showing referential integrity
- [ ] Reports demonstrating functionality

**How to Verify:**
1. Open MySQL/phpMyAdmin
2. Import bristol_events.sql
3. Check that database creates without errors
4. Run verification queries at end of script
5. Verify all 8 tables exist
6. Verify sample data is present

**Verification:** Script executes completely without errors

---

## OVERALL QUALITY CHECKS

### Documentation
- [ ] README.md is comprehensive
- [ ] ERD documentation is detailed
- [ ] SQL script is well-commented
- [ ] File structure is organized

### Code Quality
- [ ] HTML is properly indented
- [ ] CSS is organized by sections
- [ ] JavaScript is functional
- [ ] SQL follows best practices

### Completeness
- [ ] All required files present
- [ ] No missing assets or links
- [ ] Project meets all requirements
- [ ] Ready for submission

---

## SCORING GUIDE

### Week 8 - Review Point 1 (10 marks)
- Web pages for all needs: 1.5 marks
- Creative HTML, logical flow: 2.5 marks
- Responsive (3 sizes): 2.5 marks
- Nice look & feel: 2.5 marks
- Validated syntax: 1 mark

### Term 2 Week 2 - Review Point (10 marks)
- ERD with all requirements: 3 marks
- Database in 1NF with examples: 1 mark
- Database in 2NF: 1 mark
- 2NF transformation examples: 1 mark
- Database in 3NF: 1 mark
- 3NF transformation examples: 1 mark
- Error-free SQL with referential integrity: 2 marks

**Total Progress Reviews: 20 marks**

---

## NOTES FOR TUTOR

### Quick Verification Steps:

**For HTML/CSS Review:**
1. Open index.html in browser
2. Check responsive design (F12, device toolbar)
3. Navigate through all pages
4. Verify all links work
5. Check mobile menu functionality

**For Database Review:**
1. Read ERD_AND_NORMALIZATION.md
2. Verify normalization examples are clear
3. Import bristol_events.sql into MySQL
4. Check that it creates without errors
5. Run verification queries

### Common Issues to Check:
- Mobile menu toggle works
- All pages are linked
- No 404 errors
- Database creates successfully
- Foreign keys work correctly
- Sample data follows constraints

---

**Prepared by:** [Your Name]
**Student ID:** [Your Student ID]
**Date:** January 28, 2026
