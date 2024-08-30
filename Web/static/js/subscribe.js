// subscribe.js

document.addEventListener('DOMContentLoaded', function() {
    // Add any JavaScript functionality needed for the subscribe page here
    console.log('Subscribe page loaded');
    
    // Example: Form validation or enhancements
    const form = document.querySelector('.subscribe-form');
    form.addEventListener('submit', function(event) {
        const emailInput = document.getElementById('email');
        if (!emailInput.value) {
            alert('Please enter a valid email address.');
            event.preventDefault();
        }
    });
});
