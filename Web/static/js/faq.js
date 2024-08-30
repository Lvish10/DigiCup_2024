// faq.js

document.addEventListener('DOMContentLoaded', function () {
    // Add any JavaScript code needed for the FAQ page
    console.log('FAQ page loaded');
    
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
