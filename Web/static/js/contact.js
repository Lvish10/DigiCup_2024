// Contact Page JavaScript

// Handle form submission
document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    var formData = new FormData(this);
    
    // Example of handling form data (you may want to send it via AJAX or a different method)
    console.log('Name:', formData.get('name'));
    console.log('Email:', formData.get('email'));
    console.log('Message:', formData.get('message'));
    
    // Show a message to the user (for demonstration purposes)
    alert('Thank you for contacting us! We will get back to you soon.');
});
