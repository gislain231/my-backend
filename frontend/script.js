// Global variables
let currentUser = null;
let vehicles = [];
let services = [];

// API Base URL
const API_BASE_URL = 'http://127.0.0.1:5000';

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize the application
function initializeApp() {
    setupNavigation();
    setupModals();
    setupForms();
    loadVehicles();
    loadServices();
    setupSmoothScrolling();
}

// Navigation functionality
function setupNavigation() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Modal functionality
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
    document.body.style.overflow = 'hidden';
    // Reset confirmation and show form
    if (modalId === 'registerModal') {
        document.getElementById('registerConfirmation').classList.remove('active');
        document.getElementById('registerConfirmation').innerHTML = '';
        document.getElementById('registerForm').style.display = 'block';
    }
    if (modalId === 'bookingModal') {
        document.getElementById('bookingConfirmation').classList.remove('active');
        document.getElementById('bookingConfirmation').innerHTML = '';
        document.getElementById('bookingForm').style.display = 'block';
    }
    if (modalId === 'detailingModal') {
        document.getElementById('detailingConfirmation').classList.remove('active');
        document.getElementById('detailingConfirmation').innerHTML = '';
        document.getElementById('detailingForm').style.display = 'block';
    }
    if (modalId === 'loginModal') {
        document.getElementById('loginConfirmation').classList.remove('active');
        document.getElementById('loginConfirmation').innerHTML = '';
        document.getElementById('loginForm').style.display = 'block';
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            closeModal(modal.id);
        }
    });
}

// Form handling
document.addEventListener('DOMContentLoaded', function() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const userType = document.getElementById('loginUserType').value;
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            if (userType === 'provider') {
                // Provider login
                const providers = JSON.parse(localStorage.getItem('providers') || '[]');
                const provider = providers.find(p => p.businessEmail === email && p.businessPassword === password);
                if (!provider) {
                    showLoginConfirmation('loginConfirmation', 'Incorrect provider email or password.', false);
                    return;
                }
                if (!provider.approved) {
                    showLoginConfirmation('loginConfirmation', 'Your business is not yet approved. Please wait for admin approval.', false);
                    return;
                }
                localStorage.setItem('providerAuth', email);
                showLoginConfirmation('loginConfirmation', 'Provider login successful! <br><button class="btn btn-primary" onclick="window.location.href=\'provider-setup.html\'">Go to Provider Setup</button>', true);
                loginForm.style.display = 'none';
            } else {
                // Customer login (demo: only test@green.com)
                if (email === 'test@green.com' && password === 'test1234') {
                    showLoginConfirmation('loginConfirmation', 'Login successful! Welcome back. <br><button class="btn btn-primary" id="goToProvidersBtn">Choose a Provider</button>', true);
                    loginForm.style.display = 'none';
                    showProvidersNav();
                    setTimeout(() => {
                        const btn = document.getElementById('goToProvidersBtn');
                        if (btn) btn.onclick = function() {
                            closeModal('loginModal');
                            window.location.href = 'service-providers.html';
                        };
                    }, 100);
                } else {
                    showLoginConfirmation('loginConfirmation', 'Incorrect email or password. Please try again.', false);
                }
            }
        });
    }

    function goToProviders() {
        closeModal('loginModal');
        window.location.href = 'service-providers.html';
    }

    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const userType = document.getElementById('registerUserType').value;
            const name = document.getElementById('registerName').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const phone = document.getElementById('registerPhone').value;
            if (userType === 'provider') {
                // Provider registration
                const providers = JSON.parse(localStorage.getItem('providers') || '[]');
                providers.push({
                    businessName: name,
                    businessEmail: email,
                    businessPassword: password,
                    businessPhone: phone,
                    businessServiceType: '',
                    approved: false
                });
                localStorage.setItem('providers', JSON.stringify(providers));
                localStorage.setItem('providerAuth', email);
                showConfirmation('registerConfirmation', 'Provider registration successful! Please wait for approval. <br>You will be redirected to setup...', true);
                registerForm.style.display = 'none';
                setTimeout(() => {
                    let providers = JSON.parse(localStorage.getItem('providers') || '[]');
                    let idx = providers.findIndex(p => p.businessEmail === email);
                    if (idx !== -1) {
                        providers[idx].approved = true;
                        localStorage.setItem('providers', JSON.stringify(providers));
                        window.location.href = 'provider-setup.html';
                    }
                }, 2000);
            } else {
                // Customer registration
                localStorage.setItem('userEmail', email);
                showConfirmation('registerConfirmation', 'Registration successful! Welcome to GreenShare. <br>You will be redirected to login...', true);
                registerForm.style.display = 'none';
                setTimeout(() => {
                    closeModal('registerModal');
                    openModal('loginModal');
                }, 1800);
            }
        });
    }

    // Booking form
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const serviceType = document.getElementById('bookingType').value;
            const pickupLocation = document.getElementById('pickupLocation').value;
            const destination = document.getElementById('destination').value;
            const pickupDate = document.getElementById('pickupDate').value;
            
            // Simulate API call
            console.log('Booking attempt:', { serviceType, pickupLocation, destination, pickupDate });
            showConfirmation('bookingConfirmation', 'Booking successful! Thank you for sharing and helping others. <br><button class="btn btn-primary" onclick="closeModal(\'bookingModal\')">Done</button>');
            bookingForm.style.display = 'none';
        });
    }

    // Detailing form
    const detailingForm = document.getElementById('detailingForm');
    if (detailingForm) {
        detailingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const serviceType = document.getElementById('serviceType').value;
            const vehicleType = document.getElementById('vehicleType').value;
            const serviceDate = document.getElementById('serviceDate').value;
            const serviceAddress = document.getElementById('serviceAddress').value;
            
            // Simulate API call
            console.log('Detailing booking:', { serviceType, vehicleType, serviceDate, serviceAddress });
            showConfirmation('detailingConfirmation', 'Detailing service booked! Our eco team will contact you soon. <br><button class="btn btn-primary" onclick="closeModal(\'detailingModal\')">Done</button>');
            detailingForm.style.display = 'none';
        });
    }

    // Contact form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // Simulate API call
            console.log('Contact form submission:', { name, email, message });
            alert('Thank you for your message! We will get back to you soon.');
            contactForm.reset();
        });
    }

    // Provider Login modal logic
    window.openProviderLoginModal = function() {
        document.getElementById('providerLoginModal').style.display = 'block';
        document.body.style.overflow = 'hidden';
        document.getElementById('providerLoginConfirmation').innerHTML = '';
        document.getElementById('providerLoginForm').style.display = 'block';
    };

    const providerLoginForm = document.getElementById('providerLoginForm');
    if (providerLoginForm) {
        providerLoginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('providerLoginEmail').value;
            const password = document.getElementById('providerLoginPassword').value;
            const providers = JSON.parse(localStorage.getItem('providers') || '[]');
            const provider = providers.find(p => p.businessEmail === email && p.businessPassword === password);
            if (!provider) {
                showProviderRegisterConfirmation('providerLoginConfirmation', 'Incorrect email or password.', false);
                return;
            }
            if (!provider.approved) {
                showProviderRegisterConfirmation('providerLoginConfirmation', 'Your business is not yet approved. Please wait for admin approval.', false);
                return;
            }
            // Set provider session and redirect
            localStorage.setItem('providerAuth', email);
            window.location.href = 'provider-setup.html';
        });
    }
});

// Smooth scrolling for navigation links
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

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(102, 126, 234, 0.2)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 2px 20px rgba(102, 126, 234, 0.1)';
    }
});

// Add loading animation to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
        if (this.type === 'submit') {
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 1000);
        }
    });
});

// Add hover effects to service cards
document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add parallax effect to hero section
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.service-card, .about-content, .contact-form').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add keyboard navigation for modals
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal[style*="display: block"]');
        openModals.forEach(modal => {
            closeModal(modal.id);
        });
    }
});

// Add form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ff6b6b';
            isValid = false;
        } else {
            input.style.borderColor = '#e1e5e9';
        }
    });
    
    return isValid;
}

// Add form validation to all forms
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!validateForm(this)) {
            e.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
});

// Add loading states
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 2000);
}

// Add loading to submit buttons
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton) {
            showLoading(submitButton);
        }
    });
});

// Load vehicles from API
async function loadVehicles() {
    try {
        const response = await fetch(`${API_BASE_URL}/vehicles`);
        if (response.ok) {
            vehicles = await response.json();
            displayVehicles();
        }
    } catch (error) {
        console.error('Error loading vehicles:', error);
        // Load sample vehicles if API is not available
        loadSampleVehicles();
    }
}

function loadSampleVehicles() {
    vehicles = [
        {
            id: 1,
            make: 'Toyota',
            model: 'Camry',
            year: 2020,
            daily_rate: 50.00,
            hourly_rate: 10.00,
            vehicle_type: 'sedan',
            seating_capacity: 5,
            is_available: true
        },
        {
            id: 2,
            make: 'Honda',
            model: 'Civic',
            year: 2019,
            daily_rate: 45.00,
            hourly_rate: 8.00,
            vehicle_type: 'sedan',
            seating_capacity: 5,
            is_available: true
        },
        {
            id: 3,
            make: 'Ford',
            model: 'Escape',
            year: 2021,
            daily_rate: 60.00,
            hourly_rate: 12.00,
            vehicle_type: 'suv',
            seating_capacity: 5,
            is_available: true
        }
    ];
    displayVehicles();
}

function displayVehicles() {
    const vehiclesGrid = document.getElementById('vehicles-grid');
    if (!vehiclesGrid) return;

    vehiclesGrid.innerHTML = vehicles.map(vehicle => `
        <div class="vehicle-card">
            <div class="vehicle-image">
                <i class="fas fa-car"></i>
            </div>
            <div class="vehicle-info">
                <h3>${vehicle.make} ${vehicle.model}</h3>
                <div class="vehicle-details">
                    <span>${vehicle.year}</span>
                    <span>${vehicle.vehicle_type}</span>
                    <span>${vehicle.seating_capacity} seats</span>
                </div>
                <div class="vehicle-price">
                    $${vehicle.daily_rate}/day
                </div>
                <button class="btn btn-primary" onclick="bookVehicle(${vehicle.id})">
                    Book Now
                </button>
            </div>
        </div>
    `).join('');
}

function bookVehicle(vehicleId) {
    if (!currentUser) {
        showNotification('Please login to book a vehicle', 'error');
        openModal('login-modal');
        return;
    }
    openModal('booking-modal');
}

// Load services from API
async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/detailing/services`);
        if (response.ok) {
            services = await response.json();
        }
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

// Smooth scrolling
function setupSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Update UI after login
function updateUIAfterLogin() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu && currentUser) {
        // Update navigation to show user info
        const loginBtn = navMenu.querySelector('.btn-primary');
        if (loginBtn) {
            loginBtn.textContent = `Welcome, ${currentUser.first_name}`;
            loginBtn.onclick = () => showUserProfile();
        }
    }
}

function showUserProfile() {
    // This would open a user profile modal or redirect to a profile page
    showNotification('Profile feature coming soon!', 'info');
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 3000;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);

    // Add to page
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Check if user is logged in on page load
function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    if (token) {
        // Verify token with backend
        fetch(`${API_BASE_URL}/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Token invalid');
        })
        .then(data => {
            currentUser = data;
            updateUIAfterLogin();
        })
        .catch(error => {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        });
    }
}

// Initialize auth check
checkAuthStatus();

// Helper to show confirmation in modal
function showConfirmation(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = message;
        el.classList.add('active');
        // Scroll modal to confirmation
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Helper for login confirmation/error
function showLoginConfirmation(elementId, message, success) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = message;
        el.classList.add('active');
        el.style.background = success ? '#eafde6' : '#ffeaea';
        el.style.color = success ? '#234d20' : '#b00020';
        el.style.border = success ? '1px solid #a8e063' : '1px solid #b00020';
        // Scroll modal to confirmation
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Helper for provider registration confirmation
function showProviderRegisterConfirmation(elementId, message, success) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = message;
        el.classList.add('active');
        el.style.background = success ? '#eafde6' : '#ffeaea';
        el.style.color = success ? '#234d20' : '#b00020';
        el.style.border = success ? '1px solid #a8e063' : '1px solid #b00020';
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Export functions for global access
window.openModal = openModal;
window.closeModal = closeModal;
window.switchModal = switchModal;
window.scrollToSection = scrollToSection;
window.bookVehicle = bookVehicle; 

// Hide Providers nav on load
window.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('providersNav')) {
        document.getElementById('providersNav').style.display = 'none';
    }
});

// Show Providers nav after successful login
function showProvidersNav() {
    const providersNav = document.getElementById('providersNav');
    if (providersNav) {
        providersNav.style.display = 'block';
    }
} 