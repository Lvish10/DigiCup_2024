// terms.js

document.addEventListener('DOMContentLoaded', function () {
    // Add any JavaScript code needed for the Terms and Conditions page
    console.log('Terms and Conditions page loaded');
    
    // Example: Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
