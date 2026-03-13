/* =============================================
   BRISTOL EVENTS - JAVASCRIPT
   Student ID: [Your Student ID]
   Interactive Features & Animations
   ============================================= */

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!hamburger.contains(event.target) && !navMenu.contains(event.target)) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });

        // Close menu when clicking a link
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }
});

// Smooth Scroll for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Scroll-triggered Animations
function revealOnScroll() {
    const elements = document.querySelectorAll('.event-card, .category-card');
    const windowHeight = window.innerHeight;
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
            element.classList.add('fade-in');
        }
    });
}

// Run on load and scroll
window.addEventListener('load', revealOnScroll);
window.addEventListener('scroll', revealOnScroll);

// Auto-hide Flash Messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(400px)';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
        
        // Click to dismiss
        message.addEventListener('click', function() {
            this.style.opacity = '0';
            this.style.transform = 'translateX(400px)';
            setTimeout(() => {
                this.remove();
            }, 300);
        });
    });
});

// Image Loading Error Handler
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.event-image');
    
    images.forEach(img => {
        img.addEventListener('error', function() {
            // If image fails to load, show gradient background
            this.style.display = 'none';
            this.parentElement.style.background = 'linear-gradient(135deg, #ff6b9d 0%, #c44569 100%)';
        });
    });
});

// Form Validation Enhancement
function validateBookingForm(form) {
    const numTickets = parseInt(form.querySelector('#num_tickets').value);
    
    if (numTickets < 1) {
        alert('Please select at least 1 ticket! 🎟️');
        return false;
    }
    
    if (numTickets > 10) {
        alert('Maximum 10 tickets per booking! 💝');
        return false;
    }
    
    return true;
}

// Add to Event Card Click Handler
document.addEventListener('DOMContentLoaded', function() {
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach(card => {
        // Prevent click when clicking on buttons inside card
        const buttons = card.querySelectorAll('a, button');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        });
    });
});

// Loading Indicator for Forms
function showLoading(button) {
    button.disabled = true;
    button.innerHTML = '⏳ Processing...';
}

// Apply to all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                showLoading(submitButton);
            }
        });
    });
});

// Prevent Double Booking
let bookingInProgress = false;

function preventDoubleBooking(form) {
    if (bookingInProgress) {
        alert('Booking already in progress! Please wait... ✨');
        return false;
    }
    
    bookingInProgress = true;
    
    setTimeout(() => {
        bookingInProgress = false;
    }, 3000);
    
    return true;
}

// Add sparkle effect on hover (optional fun feature!)
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-book');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Countdown to Event (optional feature)
function updateCountdown(eventDateString, elementId) {
    const eventDate = new Date(eventDateString).getTime();
    
    const updateTimer = () => {
        const now = new Date().getTime();
        const distance = eventDate - now;
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `${days}d ${hours}h ${minutes}m`;
        }
        
        if (distance < 0) {
            if (element) element.innerHTML = 'Event Started!';
            return;
        }
    };
    
    updateTimer();
    setInterval(updateTimer, 60000); // Update every minute
}

// Initialize on page load
console.log('🎉 Bristol Events Website Loaded! Have fun booking! 💕');
