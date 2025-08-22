// Booking system variables
let selectedProvider = null;
let selectedService = null;
let selectedPrice = 0;
let selectedPaymentMethod = null;
let currentStep = 1;
let isUserRegistered = false; // This would be checked against backend

// Initialize booking system
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is registered (simulate API call)
    checkUserRegistration();
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('serviceDate').min = today;
});

// Check if user is registered
function checkUserRegistration() {
    // Simulate checking user registration status
    // In real app, this would be an API call
    const userEmail = localStorage.getItem('userEmail');
    isUserRegistered = userEmail && userEmail !== '';
    console.log('User registered:', isUserRegistered);
}

// Select provider and open booking modal
function selectProvider(providerName, serviceType, price) {
    selectedProvider = providerName;
    selectedService = serviceType;
    selectedPrice = price;
    
    // Open booking modal
    document.getElementById('bookingModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Reset to first step
    showStep(1);
}

// Close booking modal
function closeBookingModal() {
    document.getElementById('bookingModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    resetBookingForm();
}

// Show specific step
function showStep(stepNumber) {
    currentStep = stepNumber;
    
    // Hide all forms
    document.querySelectorAll('.booking-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Show current form
    document.getElementById(getFormId(stepNumber)).classList.add('active');
    
    // Update step indicators
    updateStepIndicators(stepNumber);
}

// Get form ID for step
function getFormId(stepNumber) {
    const forms = ['detailsForm', 'paymentForm', 'confirmForm'];
    return forms[stepNumber - 1];
}

// Update step indicators
function updateStepIndicators(activeStep) {
    for (let i = 1; i <= 3; i++) {
        const step = document.getElementById(`step${i}`);
        step.classList.remove('active', 'completed');
        
        if (i === activeStep) {
            step.classList.add('active');
        } else if (i < activeStep) {
            step.classList.add('completed');
        }
    }
}

// Next step
function nextStep(stepNumber) {
    if (validateCurrentStep()) {
        if (stepNumber === 3) {
            generateBookingSummary();
        }
        showStep(stepNumber);
    }
}

// Previous step
function prevStep(stepNumber) {
    showStep(stepNumber);
}

// Validate current step
function validateCurrentStep() {
    if (currentStep === 1) {
        return validateDetails();
    } else if (currentStep === 2) {
        return validatePayment();
    }
    return true;
}

// Validate details form
function validateDetails() {
    const requiredFields = ['fullName', 'email', 'phone', 'serviceDate'];
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            field.style.borderColor = '#ff6b6b';
            isValid = false;
        } else {
            field.style.borderColor = '#e1e5e9';
        }
    });
    
    if (!isValid) {
        alert('Please fill in all required fields.');
    }
    
    return isValid;
}

// Validate payment method
function validatePayment() {
    if (!selectedPaymentMethod) {
        alert('Please select a payment method.');
        return false;
    }
    
    if (selectedPaymentMethod === 'card') {
        const cardFields = ['cardNumber', 'expiryDate', 'cvv'];
        let isValid = true;
        
        cardFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field.value.trim()) {
                field.style.borderColor = '#ff6b6b';
                isValid = false;
            } else {
                field.style.borderColor = '#e1e5e9';
            }
        });
        
        if (!isValid) {
            alert('Please fill in all card details.');
            return false;
        }
    }
    
    return true;
}

// Select payment method
function selectPayment(method) {
    selectedPaymentMethod = method;
    
    // Update UI
    document.querySelectorAll('.payment-method').forEach(pm => {
        pm.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    
    // Show/hide card details
    const cardDetails = document.getElementById('cardDetails');
    cardDetails.style.display = method === 'card' ? 'block' : 'none';
}

// Generate booking summary
function generateBookingSummary() {
    const summary = document.getElementById('bookingSummary');
    const formData = getFormData();
    
    summary.innerHTML = `
        <h4>Booking Summary</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
            <div>
                <strong>Provider:</strong><br>
                ${selectedProvider}
            </div>
            <div>
                <strong>Service:</strong><br>
                ${selectedService}
            </div>
            <div>
                <strong>Date:</strong><br>
                ${formData.serviceDate}
            </div>
            <div>
                <strong>Total Price:</strong><br>
                $${selectedPrice}
            </div>
        </div>
        <div style="margin: 1rem 0;">
            <strong>Contact Details:</strong><br>
            ${formData.fullName}<br>
            ${formData.email}<br>
            ${formData.phone}
        </div>
        <div style="margin: 1rem 0;">
            <strong>Payment Method:</strong><br>
            ${getPaymentMethodDisplay()}
        </div>
        ${formData.specialRequests ? `<div style="margin: 1rem 0;"><strong>Special Requests:</strong><br>${formData.specialRequests}</div>` : ''}
    `;
}

// Get form data
function getFormData() {
    return {
        fullName: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value,
        serviceDate: document.getElementById('serviceDate').value,
        specialRequests: document.getElementById('specialRequests').value
    };
}

// Get payment method display text
function getPaymentMethodDisplay() {
    const methods = {
        'card': 'Credit/Debit Card',
        'paypal': 'PayPal',
        'mobile': 'Mobile Money'
    };
    return methods[selectedPaymentMethod] || 'Not selected';
}

// Confirm booking
function confirmBooking() {
    const formData = getFormData();
    
    // Check if user is registered
    if (!isUserRegistered) {
        // Redirect to registration page
        alert('Please register to complete your booking. You will be redirected to the registration page.');
        setTimeout(() => {
            closeBookingModal();
            window.location.href = 'index.html#register';
        }, 2000);
        return;
    }
    
    // Simulate payment processing
    showLoadingState();
    
    setTimeout(() => {
        // Simulate successful payment
        processBookingSuccess(formData);
    }, 3000);
}

// Show loading state
function showLoadingState() {
    const confirmBtn = document.querySelector('#confirmForm .btn-primary');
    confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing Payment...';
    confirmBtn.disabled = true;
}

// Process successful booking
function processBookingSuccess(formData) {
    // Create booking object
    const booking = {
        id: generateBookingId(),
        provider: selectedProvider,
        service: selectedService,
        price: selectedPrice,
        paymentMethod: selectedPaymentMethod,
        userDetails: formData,
        status: 'confirmed',
        createdAt: new Date().toISOString()
    };
    
    // Save booking to localStorage (in real app, this would be sent to backend)
    saveBooking(booking);
    
    // Send confirmation email
    sendConfirmationEmail(booking);
    
    // Show success message
    showBookingSuccess(booking);
}

// Generate booking ID
function generateBookingId() {
    return 'BK' + Date.now() + Math.random().toString(36).substr(2, 5).toUpperCase();
}

// Save booking
function saveBooking(booking) {
    let bookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    bookings.push(booking);
    localStorage.setItem('bookings', JSON.stringify(bookings));
}

// Send confirmation email
function sendConfirmationEmail(booking) {
    // In a real app, this would be an API call to your backend
    console.log('Sending confirmation email for booking:', booking.id);
    
    // Simulate email sending
    const emailContent = `
        Subject: Booking Confirmation - GreenShare
        
        Dear ${booking.userDetails.fullName},
        
        Thank you for choosing GreenShare! Your booking has been confirmed.
        
        Booking Details:
        - Booking ID: ${booking.id}
        - Provider: ${booking.provider}
        - Service: ${booking.service}
        - Date: ${booking.userDetails.serviceDate}
        - Total: $${booking.price}
        
        We will contact you soon with further details.
        
        Best regards,
        The GreenShare Team
    `;
    
    console.log('Email content:', emailContent);
    
    // In real implementation, this would send to the user's email
    // For demo purposes, we'll just log it
}

// Show booking success
function showBookingSuccess(booking) {
    const confirmForm = document.getElementById('confirmForm');
    confirmForm.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
            <i class="fas fa-check-circle" style="font-size: 4rem; color: #56ab2f; margin-bottom: 1rem;"></i>
            <h3 style="color: #56ab2f;">Booking Confirmed!</h3>
            <p>Your booking has been successfully processed.</p>
            <div style="background: #f8fff8; border: 1px solid #a8e063; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;">
                <strong>Booking ID:</strong> ${booking.id}<br>
                <strong>Provider:</strong> ${booking.provider}<br>
                <strong>Service:</strong> ${booking.service}<br>
                <strong>Date:</strong> ${booking.userDetails.serviceDate}<br>
                <strong>Total:</strong> $${booking.price}
            </div>
            <p>A confirmation email has been sent to ${booking.userDetails.email}</p>
            <button class="btn btn-primary" onclick="closeBookingModal()">Done</button>
        </div>
    `;
}

// Reset booking form
function resetBookingForm() {
    selectedProvider = null;
    selectedService = null;
    selectedPrice = 0;
    selectedPaymentMethod = null;
    currentStep = 1;
    
    // Reset form fields
    document.getElementById('detailsForm').reset();
    document.getElementById('paymentForm').reset();
    
    // Reset UI
    document.querySelectorAll('.payment-method').forEach(pm => {
        pm.classList.remove('selected');
    });
    document.getElementById('cardDetails').style.display = 'none';
    
    // Reset to first step
    showStep(1);
}

// Logout function
function logout() {
    // Clear user data
    localStorage.removeItem('userEmail');
    localStorage.removeItem('access_token');
    
    // Hide Providers nav on main page if returning
    if (window.opener && window.opener.document.getElementById('providersNav')) {
        window.opener.document.getElementById('providersNav').style.display = 'none';
    }
    
    // Redirect to home page
    window.location.href = 'index.html';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('bookingModal');
    if (event.target === modal) {
        closeBookingModal();
    }
}

// Export functions for global access
window.selectProvider = selectProvider;
window.closeBookingModal = closeBookingModal;
window.nextStep = nextStep;
window.prevStep = prevStep;
window.selectPayment = selectPayment;
window.confirmBooking = confirmBooking;
window.logout = logout; 